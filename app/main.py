from fastapi import FastAPI
from app.database import Base, engine
from app.api.user_roter import router
from app.api import todo_router
from app.api import auth_router

app = FastAPI()
app.include_router(router, prefix="/api/v1")
app.include_router(todo_router.router, prefix="/api/v1")
app.include_router(auth_router.router, prefix="/api/v1")
# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API rodando"}



# terminal para rodar a api: uvicorn app.main:app --reload
