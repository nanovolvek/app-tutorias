from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"
    
    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, nullable=False)  # RUT con formato XX.XXX.XXX-X
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    curso = Column(String, nullable=False)  # Ej: "3° Básico", "1° Medio"
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    nombre_apoderado = Column(String, nullable=True)  # Nombre del apoderado
    contacto_apoderado = Column(String, nullable=True)  # Contacto del apoderado (teléfono/email)
    observaciones = Column(String, nullable=True)  # Observaciones
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla equipos
    equipo = relationship("Equipo", back_populates="estudiantes")
    # Relación con la tabla asistencia_estudiantes
    asistencia_estudiantes = relationship("AsistenciaEstudiante", back_populates="estudiante")
