from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TutorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    school_id: int

class TutorCreate(TutorBase):
    pass

class TutorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    school_id: Optional[int] = None

class Tutor(TutorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
