from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class AttendanceStatus(enum.Enum):
    ATTENDED = "asistió"
    NOT_ATTENDED = "no asistió"
    SUSPENDED = "tutoría suspendida"
    VACATION = "vacaciones/feriado"

class StudentAttendance(Base):
    __tablename__ = "student_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    week = Column(String, nullable=False)  # "semana_1", "semana_2", etc.
    status = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.NOT_ATTENDED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla students
    student = relationship("Student", back_populates="student_attendance")

class TutorAttendance(Base):
    __tablename__ = "tutor_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey("tutors.id"), nullable=False)
    week = Column(String, nullable=False)  # "semana_1", "semana_2", etc.
    status = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.NOT_ATTENDED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla tutors
    tutor = relationship("Tutor", back_populates="tutor_attendance")

# Mantener el modelo original para compatibilidad (deprecated)
class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    week = Column(String, nullable=False)  # "semana_1", "semana_2", etc.
    attended = Column(Boolean, default=False)  # True si asistió, False si no asistió
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla students
    student = relationship("Student", back_populates="attendance")
