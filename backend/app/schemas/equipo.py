from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EquipoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    colegio_id: Optional[int] = None

class EquipoCreate(EquipoBase):
    pass

class Equipo(EquipoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class EquipoConDetalles(Equipo):
    tutores: List[dict] = []
    colegio: Optional[dict] = None
