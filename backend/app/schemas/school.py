from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SchoolBase(BaseModel):
    name: str
    comuna: str

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    comuna: Optional[str] = None

class School(SchoolBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
