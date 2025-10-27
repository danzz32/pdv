# app/repositories/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import *  # Vamos criar este módulo em breve


# Nota: Os schemas (ex: schemas.user.UserCreate) serão definidos depois

class UserRepository:

    def get(self, db: Session, id: uuid.UUID) -> User | None:
        return db.query(User).filter(User.id == id).first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[type[User]]:
        return db.query(User).offset(skip).limit(limit).all()

    def create(self, db: Session, user_in: UserCreate) -> User:
        # A lógica de hash da senha ficará no 'serviço'
        db_user = User(
            email=user_in.email,
            nome=user_in.nome,
            hashed_password=user_in.password  # Assumindo que o schema tem 'password'
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, db_user: User, user_in: UserUpdate) -> User:
        # Converte o schema Pydantic para um dict
        update_data = user_in.model_dump(exclude_unset=True)

        # Lógica para não atualizar a senha se ela não for fornecida
        if "password" in update_data and update_data["password"]:
            # A lógica de hash deve estar no serviço
            db_user.hashed_password = update_data["password"]

        db_user.nome = update_data.get("nome", db_user.nome)
        db_user.email = update_data.get("email", db_user.email)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def remove(self, db: Session, id: uuid.UUID) -> User | None:
        db_user = self.get(db, id=id)
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user

# Instância (opcional, ou podemos usar Injeção de Dependência)
# user_repository = UserRepository()
