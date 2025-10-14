from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class AttendanceStatus(str, Enum):
    ATTENDED = "asistió"
    NOT_ATTENDED = "no asistió"
    SUSPENDED = "tutoría suspendida"
    VACATION = "vacaciones/feriado"

# Esquemas para asistencia de estudiantes
class StudentAttendanceBase(BaseModel):
    student_id: int
    week: str
    status: AttendanceStatus

class StudentAttendanceCreate(StudentAttendanceBase):
    pass

class StudentAttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None

class StudentAttendance(StudentAttendanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas para asistencia de tutores
class TutorAttendanceBase(BaseModel):
    tutor_id: int
    week: str
    status: AttendanceStatus

class TutorAttendanceCreate(TutorAttendanceBase):
    pass

class TutorAttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None

class TutorAttendance(TutorAttendanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas de resumen
class StudentAttendanceSummary(BaseModel):
    student_id: int
    student_name: str
    course: str
    school_name: str
    total_weeks: int
    attended_weeks: int
    attendance_percentage: float
    weekly_attendance: dict  # {"semana_1": "asistió", "semana_2": "no asistió", ...}

class TutorAttendanceSummary(BaseModel):
    tutor_id: int
    tutor_name: str
    school_name: str
    total_weeks: int
    attended_weeks: int
    attendance_percentage: float
    weekly_attendance: dict  # {"semana_1": "asistió", "semana_2": "no asistió", ...}

# Esquemas legacy para compatibilidad
class AttendanceBase(BaseModel):
    student_id: int
    week: str
    attended: bool

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    attended: Optional[bool] = None

class Attendance(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
