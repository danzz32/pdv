# app/main.py (ATUALIZADO)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar Base e engine
from app.database import Base, engine
# Importar todos os seus módulos de modelo
from app.models import (
    item, user, categoria, pedido, pedido_item,
    grupo_modificador, opcao_modificador, pedido_item_modificador
)

# Importar seus roteadores
from app.routes import items, users, categorias, pedidos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PDV - Cardápio Online API",
    description="Backend para o sistema de Ponto de Venda e Cardápio Online.",
    version="0.1.0",
    # Adiciona documentação para as Tags
    openapi_tags=[
        {"name": "Pedidos", "description": "Operações para criar e gerenciar pedidos."},
        {"name": "Itens do Cardápio", "description": "Gerenciamento do cardápio (itens, preços, etc)."},
        {"name": "Categorias", "description": "Gerenciamento das categorias dos itens."},
        {"name": "Usuários", "description": "Registro e gerenciamento de usuários."},
    ]
)

# Configuração do CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir os roteadores
app.include_router(pedidos.router)
app.include_router(items.router)
app.include_router(categorias.router)
app.include_router(users.router)


# (Quando tiver rotas de login/auth, inclua-as também)

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "PDV Backend is running!"}
