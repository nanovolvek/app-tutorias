from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    comuna = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    tutors = relationship("Tutor", back_populates="school")
    students = relationship("Student", back_populates="school")
