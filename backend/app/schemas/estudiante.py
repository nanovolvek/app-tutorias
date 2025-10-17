from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EstudianteBase(BaseModel):
    rut: str
    nombre: str
    apellido: str
    curso: str
    equipo_id: int
    nombre_apoderado: Optional[str] = None
    contacto_apoderado: Optional[str] = None
    observaciones: Optional[str] = None

class EstudianteCreate(EstudianteBase):
    pass

class Estudiante(EstudianteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
