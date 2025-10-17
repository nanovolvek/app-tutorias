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

class ColegioInfo(BaseModel):
    id: int
    nombre: str
    comuna: str

class EquipoInfo(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    colegio_id: Optional[int] = None
    colegio: Optional[ColegioInfo] = None

class Estudiante(EstudianteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    equipo: Optional[EquipoInfo] = None
    
    class Config:
        from_attributes = True
