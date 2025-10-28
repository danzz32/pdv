"""
Define a camada de serviço (lógica de negócios) para 'Pedido'.

Esta é a classe de serviço mais complexa, responsável por:
1. Validar e calcular o custo total de um novo pedido.
2. Coordenar a criação de um Pedido e seus sub-itens
   (PedidoItem, PedidoItemModificador) nos respectivos repositórios.
"""

# 1. Importações da biblioteca padrão
from typing import Dict, Any, Tuple, Optional
import uuid

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

# 3. Importações locais da aplicação
from app.schemas.pedido import Pedido, PedidoCreate, PedidoCreateAPI
from app.schemas.user import User
from app.schemas.pedido_item import PedidoItemCreate
from app.schemas.pedido_item_modificador import PedidoItemModificadorCreate

# Modelos ORM (para anotações de tipo claras)
from app.models.pedido import Pedido as PedidoModel
from app.models.item import Item as ItemModel
from app.models.opcao_modificador import OpcaoModificador as OpcaoModel

# Importações absolutas
from app.repositories.pedido import PedidoRepository
from app.repositories.item import ItemRepository
from app.repositories.opcao_modificador import OpcaoModificadorRepository
from app.repositories.pedido_item import PedidoItemRepository
from app.repositories.pedido_item_modificador import (
    PedidoItemModificadorRepository
)


# pylint: disable=R0903
# Desabilitamos R0903 (Too few public methods) pois esta classe
# tem uma responsabilidade única (criar pedidos) e 1-2 métodos
# públicos são aceitáveis para esse padrão.
class PedidoService:
    """Camada de serviço para coordenar a criação de Pedidos."""

    # pylint: disable=R0913
    # Desabilitamos R0913 (Too many arguments) pois 6 argumentos
    # é aceitável para injeção de dependência (DI) de repositórios.
    def __init__(
            self,
            pedido_repo: PedidoRepository = Depends(PedidoRepository),
            item_repo: ItemRepository = Depends(ItemRepository),
            opcao_repo: OpcaoModificadorRepository = Depends(OpcaoModificadorRepository),
            pedido_item_repo: PedidoItemRepository = Depends(PedidoItemRepository),
            pedido_item_mod_repo: PedidoItemModificadorRepository = Depends(
                PedidoItemModificadorRepository
            ),
    ):
        """Inicializa o serviço injetando todos os repositórios necessários."""
        self.pedido_repo = pedido_repo
        self.item_repo = item_repo
        self.opcao_repo = opcao_repo
        self.pedido_item_repo = pedido_item_repo
        self.pedido_item_mod_repo = pedido_item_mod_repo

    def _get_pedido_creator_info(
            self, current_user: Optional[User], nome_anonimo: Optional[str]
    ) -> Tuple[Optional[uuid.UUID], Optional[str]]:
        """
        Valida e extrai a informação do cliente (logado ou anônimo).
        Retorna (usuario_id, nome_anonimo_final).
        """
        if current_user:
            return current_user.id, None

        if not nome_anonimo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome do cliente é obrigatório para pedidos anônimos."
            )
        return None, nome_anonimo

    def _persist_pedido_details(
            self,
            db: Session,
            db_pedido: PedidoModel,
            pedido_in: PedidoCreateAPI,
            dados_db: Dict[str, Any]
    ):
        """
        Cria e salva os PedidoItems e PedidoItemModificadores associados.
        (Refatorado de 'create_pedido' para resolver R0914 - Too many locals)
        """
        for item_input in pedido_in.itens:
            db_item: ItemModel = dados_db["itens"][item_input.item_id]

            repo_pedido_item_create = PedidoItemCreate(
                quantidade=item_input.quantidade,
                preco_unitario_base=db_item.preco_base,
                observacoes=item_input.observacoes,
                pedido_id=db_pedido.id,
                item_id=db_item.id
            )
            db_pedido_item = self.pedido_item_repo.create(
                db, pedido_item_in=repo_pedido_item_create
            )

            for mod_input in item_input.modificadores:
                db_opcao: OpcaoModel = dados_db["opcoes"][
                    mod_input.opcao_modificador_id
                ]

                repo_mod_create = PedidoItemModificadorCreate(
                    preco_cobrado=db_opcao.preco_adicional,
                    pedido_item_id=db_pedido_item.id,
                    opcao_modificador_id=db_opcao.id
                )
                self.pedido_item_mod_repo.create(db, mod_in=repo_mod_create)

    def _validar_e_calcular_total(
            self, db: Session, pedido_in: PedidoCreateAPI
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Valida todos os itens e modificadores, calcula o preço total.
        Retorna (valor_total, dados_validados_db).
        """
        valor_total_pedido = 0.0
        # dados_validados armazena os objetos do DB para evitar
        # buscá-los novamente durante a persistência.
        dados_validados: Dict[str, Any] = {"itens": {}, "opcoes": {}}

        if not pedido_in.itens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O pedido não pode estar vazio."
            )

        for item_input in pedido_in.itens:
            db_item = self.item_repo.get(db, id=item_input.item_id)
            if not db_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item ID {item_input.item_id} não encontrado."
                )
            if not db_item.disponivel:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Item '{db_item.nome}' está indisponível."
                )

            dados_validados["itens"][db_item.id] = db_item
            preco_item_final = db_item.preco_base

            opcoes_ids_deste_item = {
                op.id for grupo in db_item.grupos_modificadores for op in grupo.opcoes
            }

            for mod_input in item_input.modificadores:
                db_opcao = self.opcao_repo.get(
                    db, id=mod_input.opcao_modificador_id
                )
                if not db_opcao:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Opção ID {mod_input.opcao_modificador_id} não encontrada.",
                    )
                if db_opcao.id not in opcoes_ids_deste_item:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Opção '{db_opcao.nome}' não pertence ao item '{db_item.nome}'.",
                    )

                dados_validados["opcoes"][db_opcao.id] = db_opcao
                preco_item_final += db_opcao.preco_adicional

            valor_total_pedido += (preco_item_final * item_input.quantidade)

        return valor_total_pedido, dados_validados

    def create_pedido(
            self, db: Session, pedido_in: PedidoCreateAPI, current_user: Optional[User]
    ) -> PedidoModel:
        """
        Orquestra a criação de um novo pedido.

        Etapas:
        1. Valida a informação do cliente (anônimo ou logado).
        2. Valida os itens, modificadores e calcula o valor total.
        3. Cria o registro 'Pedido' principal.
        4. Cria os registros 'PedidoItem' e 'PedidoItemModificador' associados.
        5. Retorna o pedido completo.
        """

        # Etapa 1: Validar cliente
        usuario_id_final, nome_anonimo_final = self._get_pedido_creator_info(
            current_user, pedido_in.nome_cliente_anonimo
        )

        # Etapa 2: Validar itens e calcular total
        valor_total_calculado, dados_db = self._validar_e_calcular_total(
            db, pedido_in
        )

        # Etapa 3: Criar o Pedido principal
        repo_pedido_create = PedidoCreate(
            valor_total=valor_total_calculado,
            usuario_id=usuario_id_final,
            session_id=pedido_in.session_id if not current_user else None,
            forma_de_pagamento=pedido_in.forma_de_pagamento,
            nome_cliente_anonimo=nome_anonimo_final
        )
        db_pedido = self.pedido_repo.create(db, pedido_in=repo_pedido_create)

        # Etapa 4: Persistir os detalhes (Itens e Modificadores)
        self._persist_pedido_details(db, db_pedido, pedido_in, dados_db)

        # Etapa 5: Retornar o pedido completo
        db.refresh(db_pedido)
        return db_pedido
