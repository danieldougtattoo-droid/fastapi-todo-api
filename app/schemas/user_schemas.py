from pydantic import BaseModel, EmailStr, constr
from pydantic import field_validator

class UserResponse(BaseModel):
    id: int
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@field_validator('password')
def validate_password(cls, v):
    if len(v) < 6:
        raise ValueError('mínimo 6 caracteres')
    if len(v.encode('utf-8')) > 72:
        raise ValueError('máximo 72 bytes')
    return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str