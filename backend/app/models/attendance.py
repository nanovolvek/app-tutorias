from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class EstadoAsistencia(enum.Enum):
    ASISTIO = "asistió"
    NO_ASISTIO = "no asistió"
    SUSPENDIDA = "tutoría suspendida"
    VACACIONES = "vacaciones/feriado"

class AsistenciaEstudiante(Base):
    __tablename__ = "asistencia_estudiantes"
    
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    semana = Column(String, nullable=False)  # "semana_1", "semana_2", etc.
    estado = Column(Enum(EstadoAsistencia), nullable=False, default=EstadoAsistencia.NO_ASISTIO)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla estudiantes
    estudiante = relationship("Estudiante", back_populates="asistencia_estudiantes")

class AsistenciaTutor(Base):
    __tablename__ = "asistencia_tutores"
    
    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey("tutores.id"), nullable=False)
    semana = Column(String, nullable=False)  # "semana_1", "semana_2", etc.
    estado = Column(Enum(EstadoAsistencia), nullable=False, default=EstadoAsistencia.NO_ASISTIO)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla tutores
    tutor = relationship("Tutor", back_populates="asistencia_tutores")
