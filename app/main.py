from fastapi import FastAPI
from app.database import Base, engine
from app.api.user_roter import router
from app.api import todo_router
from app.api import auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://react-dashboard-auth-iota.vercel.app",
                   "https://react-dashboard-auth-agiaor7sa-danieldougtattoo-droids-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
app.include_router(todo_router.router, prefix="/api/v1")
app.include_router(auth_router.router, prefix="/api/v1")
# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API rodando"}



# terminal para rodar a api: uvicorn app.main:app --reload
