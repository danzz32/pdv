# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# pylint: disable=unused-import
from app.models import (
    item, user, categoria, pedido, pedido_item,
    grupo_modificador, opcao_modificador, pedido_item_modificador
)

# Importando rotas
from app.routes import items, users, categorias, pedidos
from app.routes import auth as auth_router  # <-- IMPORTAR ROTA DE AUTH

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PDV - Cardápio Online API",
    description="Backend para o sistema de Ponto de Venda e Cardápio Online.",
    version="0.1.0",
    # Documentação das Tags
    openapi_tags=[
        # <-- ADICIONAR NOVA TAG ---
        {"name": "Autenticação", "description": "Operações de login e gerenciamento de token."},
        {"name": "Pedidos", "description": "Operações para criar e gerenciar pedidos."},
        {"name": "Itens do Cardápio", "description": "Gerenciamento do cardápio (itens, preços, etc)."},
        {"name": "Categorias", "description": "Gerenciamento das categorias dos itens."},
        {"name": "Usuários", "description": "Registro e gerenciamento de usuários."},
    ]
)

# Configuração do CORS (Restaurando para nossas origens de dev)
origins = [
    "http://localhost:5173",  # Frontend Vite
    "http://localhost:8080",  # Docker Nginx
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo rotas
app.include_router(auth_router.router)  # <-- INCLUIR ROTA DE AUTH
app.include_router(pedidos.router)
app.include_router(items.router)
app.include_router(categorias.router)
app.include_router(users.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"status": "PDV Backend is running!"}
