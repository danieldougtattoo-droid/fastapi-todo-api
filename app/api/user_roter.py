from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user_schemas import UserCreate, UserResponse
from app.services.user_service import create_user
from app.database import get_db


router = APIRouter()

# Create user
@router.post("/users", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        novo_usuario = create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not novo_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return novo_usuario



