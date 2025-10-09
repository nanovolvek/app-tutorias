from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.tutor import Tutor
from app.models.school import School
from app.schemas.tutor import Tutor as TutorSchema, TutorCreate, TutorUpdate
from app.auth.dependencies import get_current_active_user, get_admin_user
from app.models.user import User

router = APIRouter(prefix="/tutors", tags=["tutores"])

@router.get("/", response_model=List[TutorSchema])
def get_tutors(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener lista de tutores"""
    tutors = db.query(Tutor).offset(skip).limit(limit).all()
    return tutors

@router.get("/{tutor_id}", response_model=TutorSchema)
def get_tutor(
    tutor_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un tutor por ID"""
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if tutor is None:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    return tutor

@router.post("/", response_model=TutorSchema)
def create_tutor(
    tutor: TutorCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Crear un nuevo tutor (solo administradores)"""
    # Verificar que el colegio existe
    school = db.query(School).filter(School.id == tutor.school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    db_tutor = Tutor(**tutor.dict())
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

@router.put("/{tutor_id}", response_model=TutorSchema)
def update_tutor(
    tutor_id: int, 
    tutor: TutorUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Actualizar un tutor (solo administradores)"""
    db_tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if db_tutor is None:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    # Si se actualiza el school_id, verificar que existe
    if tutor.school_id is not None:
        school = db.query(School).filter(School.id == tutor.school_id).first()
        if school is None:
            raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    update_data = tutor.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tutor, field, value)
    
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

@router.delete("/{tutor_id}")
def delete_tutor(
    tutor_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Eliminar un tutor (solo administradores)"""
    db_tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if db_tutor is None:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    db.delete(db_tutor)
    db.commit()
    return {"message": "Tutor eliminado correctamente"}
