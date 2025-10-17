from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.tutor import Tutor
from app.models.equipo import Equipo
from app.schemas.tutor import Tutor as TutorSchema, TutorCreate
from app.auth.dependencies import get_current_active_user, get_admin_user, get_tutor_user

router = APIRouter(prefix="/tutores", tags=["tutores"])

@router.get("/", response_model=List[TutorSchema])
def get_tutores(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener tutores según el rol del usuario"""
    if current_user.rol == "admin":
        # Admin puede ver todos los tutores
        tutores = db.query(Tutor).all()
    else:
        # Tutor solo puede ver tutores de su equipo
        tutores = db.query(Tutor).filter(Tutor.equipo_id == current_user.equipo_id).all()
    
    return tutores

@router.get("/{tutor_id}", response_model=TutorSchema)
def get_tutor(
    tutor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener un tutor específico"""
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tutor no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol == "tutor" and tutor.equipo_id != current_user.equipo_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este tutor"
        )
    
    return tutor

@router.post("/", response_model=TutorSchema)
def create_tutor(
    tutor: TutorCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Crear un nuevo tutor (solo administradores)"""
    # Verificar que el equipo existe
    equipo = db.query(Equipo).filter(Equipo.id == tutor.equipo_id).first()
    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    
    db_tutor = Tutor(**tutor.dict())
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor
