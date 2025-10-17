from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Colegio(Base):
    __tablename__ = "colegios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    comuna = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con equipos
    equipos = relationship("Equipo", back_populates="colegio")
