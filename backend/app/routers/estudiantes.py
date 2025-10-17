from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.student import Estudiante
from app.models.equipo import Equipo
from app.schemas.estudiante import Estudiante as EstudianteSchema, EstudianteCreate
from app.auth.dependencies import get_current_active_user, get_admin_user, get_tutor_user

router = APIRouter(prefix="/estudiantes", tags=["estudiantes"])

@router.get("/", response_model=List[EstudianteSchema])
def get_estudiantes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener estudiantes según el rol del usuario"""
    if current_user.rol == "admin":
        # Admin puede ver todos los estudiantes
        estudiantes = db.query(Estudiante).all()
    else:
        # Tutor solo puede ver estudiantes de su equipo
        estudiantes = db.query(Estudiante).filter(Estudiante.equipo_id == current_user.equipo_id).all()
    
    return estudiantes

@router.get("/{estudiante_id}", response_model=EstudianteSchema)
def get_estudiante(
    estudiante_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener un estudiante específico"""
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol == "tutor" and estudiante.equipo_id != current_user.equipo_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este estudiante"
        )
    
    return estudiante

@router.post("/", response_model=EstudianteSchema)
def create_estudiante(
    estudiante: EstudianteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Crear un nuevo estudiante (solo administradores)"""
    # Verificar que el equipo existe
    equipo = db.query(Equipo).filter(Equipo.id == estudiante.equipo_id).first()
    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    
    db_estudiante = Estudiante(**estudiante.dict())
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante
