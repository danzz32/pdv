# app/services/pedido.py (CORRIGIDO)
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends  # Mantenha o Depends

from app.schemas.pedido import *
from app.schemas.user import *
from app.schemas.pedido_item import *
from app.schemas.pedido_item_modificador import *

from ..repositories.pedido import PedidoRepository
from ..repositories.item import ItemRepository
from ..repositories.opcao_modificador import OpcaoModificadorRepository
from ..repositories.pedido_item import PedidoItemRepository
from ..repositories.pedido_item_modificador import PedidoItemModificadorRepository


class PedidoService:

    # --- CORREÇÃO AQUI ---
    # O __init__ do serviço deve receber as classes
    # O FastAPI injetará as dependências
    def __init__(self,
                 pedido_repo: PedidoRepository = Depends(PedidoRepository),
                 item_repo: ItemRepository = Depends(ItemRepository),
                 opcao_repo: OpcaoModificadorRepository = Depends(OpcaoModificadorRepository),
                 pedido_item_repo: PedidoItemRepository = Depends(PedidoItemRepository),
                 pedido_item_mod_repo: PedidoItemModificadorRepository = Depends(PedidoItemModificadorRepository)
                 ):
        self.pedido_repo = pedido_repo
        self.item_repo = item_repo
        self.opcao_repo = opcao_repo
        self.pedido_item_repo = pedido_item_repo
        self.pedido_item_mod_repo = pedido_item_mod_repo

    # ... (o resto do seu arquivo _validar_e_calcular_total e create_pedido) ...
    # ... (não precisa mudar o resto da lógica) ...
    def _validar_e_calcular_total(self, db: Session, pedido_in: PedidoCreateAPI) -> (float, dict):
        # ... (código existente) ...
        valor_total_pedido = 0.0
        dados_validados = {"itens": {}, "opcoes": {}}
        if not pedido_in.itens:
            raise HTTPException(status_code=400, detail="O pedido não pode estar vazio.")
        for item_input in pedido_in.itens:
            db_item = self.item_repo.get(db, id=item_input.item_id)
            if not db_item:
                raise HTTPException(status_code=404, detail=f"Item ID {item_input.item_id} não encontrado.")
            if not db_item.disponivel:
                raise HTTPException(status_code=400, detail=f"Item '{db_item.nome}' está indisponível.")
            dados_validados["itens"][db_item.id] = db_item
            preco_item_final = db_item.preco_base
            opcoes_ids_deste_item = {op.id for grupo in db_item.grupos_modificadores for op in grupo.opcoes}
            for mod_input in item_input.modificadores:
                db_opcao = self.opcao_repo.get(db, id=mod_input.opcao_modificador_id)
                if not db_opcao:
                    raise HTTPException(status_code=404,
                                        detail=f"Opção ID {mod_input.opcao_modificador_id} não encontrada.")
                if db_opcao.id not in opcoes_ids_deste_item:
                    raise HTTPException(status_code=400,
                                        detail=f"Opção '{db_opcao.nome}' não pertence ao item '{db_item.nome}'.")
                dados_validados["opcoes"][db_opcao.id] = db_opcao
                preco_item_final += db_opcao.preco_adicional
            valor_total_pedido += (preco_item_final * item_input.quantidade)
        return valor_total_pedido, dados_validados

    def create_pedido(self, db: Session, pedido_in: PedidoCreateAPI,
                      current_user: User | None):
        # ... (código existente) ...
        usuario_id_final = None
        nome_anonimo_final = None
        if current_user:
            usuario_id_final = current_user.id
        else:
            if not pedido_in.nome_cliente_anonimo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="O nome do cliente é obrigatório para pedidos anônimos."
                )
            nome_anonimo_final = pedido_in.nome_cliente_anonimo
        try:
            valor_total_calculado, dados_db = self._validar_e_calcular_total(db, pedido_in)
        except HTTPException as e:
            raise e
        repo_pedido_create = PedidoCreate(
            valor_total=valor_total_calculado,
            usuario_id=usuario_id_final,
            session_id=pedido_in.session_id if not current_user else None,
            forma_de_pagamento=pedido_in.forma_de_pagamento,
            nome_cliente_anonimo=nome_anonimo_final
        )
        db_pedido = self.pedido_repo.create(db, pedido_in=repo_pedido_create)
        for item_input in pedido_in.itens:
            db_item = dados_db["itens"][item_input.item_id]
            repo_pedido_item_create = PedidoItemCreate(
                quantidade=item_input.quantidade,
                preco_unitario_base=db_item.preco_base,
                observacoes=item_input.observacoes,
                pedido_id=db_pedido.id,
                item_id=db_item.id
            )
            db_pedido_item = self.pedido_item_repo.create(db, pedido_item_in=repo_pedido_item_create)
            for mod_input in item_input.modificadores:
                db_opcao = dados_db["opcoes"][mod_input.opcao_modificador_id]
                repo_mod_create = PedidoItemModificadorCreate(
                    preco_cobrado=db_opcao.preco_adicional,
                    pedido_item_id=db_pedido_item.id,
                    opcao_modificador_id=db_opcao.id
                )
                self.pedido_item_mod_repo.create(db, mod_in=repo_mod_create)
        db.refresh(db_pedido)
        return db_pedido
