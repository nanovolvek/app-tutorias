from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ColegioInfo(BaseModel):
    id: int
    nombre: str
    comuna: str

class EquipoInfo(BaseModel):
    id: int
    nombre: str
    colegio: Optional[ColegioInfo] = None

class TutorBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    equipo_id: int

class TutorCreate(TutorBase):
    pass

class Tutor(TutorBase):
    id: int
    equipo: Optional[EquipoInfo] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True