from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, nullable=False)  # RUT con formato XX.XXX.XXX-X
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    course = Column(String, nullable=False)  # Ej: "3° Básico", "1° Medio"
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    guardian_name = Column(String, nullable=True)  # Nombre del apoderado
    guardian_contact = Column(String, nullable=True)  # Contacto del apoderado (teléfono/email)
    observations = Column(String, nullable=True)  # Observaciones
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla schools
    school = relationship("School", back_populates="students")
    # Relación con la tabla attendance (deprecated)
    attendance = relationship("Attendance", back_populates="student")
    # Relación con la tabla student_attendance
    student_attendance = relationship("StudentAttendance", back_populates="student")
