from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SchoolInfo(BaseModel):
    id: int
    name: str
    comuna: str
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    rut: str
    first_name: str
    last_name: str
    course: str
    school_id: int
    guardian_name: Optional[str] = None
    guardian_contact: Optional[str] = None
    observations: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    rut: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    course: Optional[str] = None
    school_id: Optional[int] = None
    guardian_name: Optional[str] = None
    guardian_contact: Optional[str] = None
    observations: Optional[str] = None

class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class StudentWithSchool(Student):
    school: SchoolInfo

class StudentWithAttendance(StudentWithSchool):
    attendance_percentage: Optional[float] = None
