from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EquipoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EquipoCreate(EquipoBase):
    pass

class Equipo(EquipoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
