from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Contexto de hash para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)

def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")[:72]
    try:
        return pwd_context.verify(password_bytes, hashed_password)
    except UnknownHashError:
        # Hash legado/invalido no banco: trata como credencial incorreta.
        return False


def create_access_token(data: dict):
    # Não permitir que o caller sobrescreva exp/tipo (claims de segurança).
    to_encode = {k: v for k, v in data.items() if k not in ("exp", "type")}
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = {k: v for k, v in data.items() if k not in ("exp", "type")}
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    # Só aceita access nas rotas protegidas; refresh não pode ser usado como Bearer.
    if payload.get("type") != "access":
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user