from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TutorBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    equipo_id: int

class TutorCreate(TutorBase):
    pass

class Tutor(TutorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True