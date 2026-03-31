from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.schemas.user_schemas import RefreshRequest, TokenResponse

from app.database import get_db
from app.services.user_service import authenticate_user
from app.core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login de usuário",
    description="Autentica o usuário e retorna access_token e refresh_token",
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # No fluxo OAuth2, o Swagger envia "username". Aqui tratamos username como email.
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/refresh", summary="Gerar novo access token", description="Recebe um refresh token e retorna um novo access token")
def refresh(data: RefreshRequest):
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token inválido")

    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    new_access_token = create_access_token(data={"sub": email})
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.get("/me", summary="Usuário atual", description="Retorna as informações do usuário atual")
def me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "id": current_user.id,
    }

