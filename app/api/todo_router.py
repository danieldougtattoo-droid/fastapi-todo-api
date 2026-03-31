from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.todo_schemas import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import create_todo, get_todos, update_todo, delete_todo, get_one_todo
from app.core.security import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/todos", tags=["todos"])

# 1. create
@router.post("/", response_model=TodoResponse)
def create(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_todo(db, todo.title, current_user.id)


# 2. list todos
@router.get("/", response_model=list[TodoResponse])
def list_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_todos(db, current_user.id)


# 3. update
@router.put("/{todo_id}", response_model=TodoResponse)
def update(
    todo_id: int,
    data: TodoUpdate | None = Body(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data is None:
        raise HTTPException(status_code=400, detail="Envie ao menos um campo para atualizar.")
    if data.title is None and data.completed is None:
        raise HTTPException(status_code=400, detail="Nada para atualizar.")

    todo = update_todo(db, todo_id, data, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo não encontrado")
    return todo


# 4. delete
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = delete_todo(db, todo_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo não encontrado")

    return {"message": "Todo deletado com sucesso"}

# 5. get by id
@router.get("/{todo_id}", response_model=TodoResponse)
def get_one(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = get_one_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo não encontrado")
    return todo


