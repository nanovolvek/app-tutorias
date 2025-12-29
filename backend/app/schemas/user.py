from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre_completo: str
    rol: str
    equipo_id: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Usuario(UsuarioBase):
    id: int
    is_active: bool
    password_changed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    requires_password_change: Optional[bool] = False

class TokenData(BaseModel):
    email: Optional[str] = None

class ChangePassword(BaseModel):
    current_password: Optional[str] = None
    new_password: str

class RequestPasswordReset(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str
