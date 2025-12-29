from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    nombre_completo = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # "admin" o "tutor"
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=True)  # Solo para tutores
    is_active = Column(Boolean, default=True)
    password_changed = Column(Boolean, default=False, nullable=False)  # Si el usuario ha cambiado su contraseña
    password_reset_token = Column(String, nullable=True)  # Token para recuperación de contraseña
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)  # Expiración del token
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con equipo (solo para tutores)
    equipo = relationship("Equipo", back_populates="usuarios")
