from pydantic import BaseModel, EmailStr, constr

class UserResponse(BaseModel):
    id: int
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=72)

    class Config:
       from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=72)
        # Configuração para que o Pydantic modele os dados do banco de dados

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"