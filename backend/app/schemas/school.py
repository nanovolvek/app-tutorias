from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SchoolBase(BaseModel):
    nombre: str
    comuna: str

class SchoolCreate(BaseModel):
    nombre: str
    comuna: str

class SchoolUpdate(BaseModel):
    nombre: Optional[str] = None
    comuna: Optional[str] = None

class School(BaseModel):
    id: int
    nombre: str
    comuna: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True
