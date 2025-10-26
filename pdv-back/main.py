from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"projeto": "PDV-Back API"}


@app.get("/api/items")
def get_items():
    # Exemplo de rota de API
    return [
        {"id": 1, "name": "Hambúrguer"},
        {"id": 2, "name": "Batata Frita"},
        {"id": 3, "name": "Refrigerante"},
    ]
