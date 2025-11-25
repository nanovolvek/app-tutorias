from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class PorcentajeLogro(enum.Enum):
    CIEN_PORCIENTO = "100%"
    OCHENTA_PORCIENTO = "80%"
    SESENTA_PORCIENTO = "60%"
    CUARENTA_PORCIENTO = "40%"
    VEINTE_PORCIENTO = "20%"
    CERO_PORCIENTO = "0%"
    VACIO = "vacío"

class PruebaDiagnosticoEstudiante(Base):
    __tablename__ = "prueba_diagnostico_estudiantes"
    
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    unidad = Column(String, nullable=False)  # "unidad_1", "unidad_2", etc.
    modulo = Column(String, nullable=False)  # "modulo_1", "modulo_2", etc.
    resultado = Column(Enum(PorcentajeLogro), nullable=False, default=PorcentajeLogro.VACIO)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con la tabla estudiantes
    estudiante = relationship("Estudiante", back_populates="prueba_diagnostico_estudiantes")

