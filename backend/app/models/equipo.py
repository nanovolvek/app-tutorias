from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Equipo(Base):
    __tablename__ = "equipos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)  # A, B, C, ..., Z
    descripcion = Column(String, nullable=True)
    colegio_id = Column(Integer, ForeignKey("colegios.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    tutores = relationship("Tutor", back_populates="equipo")
    estudiantes = relationship("Estudiante", back_populates="equipo")
    usuarios = relationship("Usuario", back_populates="equipo")
    colegio = relationship("Colegio", back_populates="equipos")
