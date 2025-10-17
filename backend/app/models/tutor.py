from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Tutor(Base):
    __tablename__ = "tutores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla equipos
    equipo = relationship("Equipo", back_populates="tutores")
    # Relación con la tabla asistencia_tutores
    asistencia_tutores = relationship("AsistenciaTutor", back_populates="tutor")
