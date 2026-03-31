from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate
from app.core.security import hash_password, verify_password

def create_user(db: Session, user: UserCreate):

    existe_usuario = db.query(User).filter(User.email == user.email).first()
    if existe_usuario:
        return None

    hashed_password = hash_password(user.password)

    novo_usuario = User(email=user.email, password=hashed_password)

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def authenticate_user(db, email: str, password: str):
    usuario = db.query(User).filter(User.email == email).first()
    if not usuario:
        return None

    if not verify_password(password, usuario.password):
        return None
    return usuario