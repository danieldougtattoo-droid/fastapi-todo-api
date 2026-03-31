from sqlalchemy.orm import Session
from app.models.todo_model import Todo
from app.schemas.todo_schemas import TodoUpdate

def create_todo(db: Session, title: str, user_id: int):
    todo = Todo(title=title, user_id=user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def get_todos(db: Session, user_id: int):
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def get_one_todo(db: Session, todo_id: int, user_id: int):
    return (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == user_id)
        .first()
    )

def update_todo(db: Session, todo_id: int, data: TodoUpdate, user_id: int):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == user_id)
        .first()
    )
    if not todo:
        return None

    if data.title is not None:
        todo.title = data.title
    if data.completed is not None:
        todo.completed = data.completed

    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int, user_id: int):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == user_id)
        .first()
    )

    if not todo:
        return False

    db.delete(todo)
    db.commit()
    return True
    