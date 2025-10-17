from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.equipo import Equipo
from app.models.tutor import Tutor
from app.models.school import Colegio
from app.schemas.equipo import Equipo as EquipoSchema, EquipoCreate, EquipoConDetalles
from app.auth.dependencies import get_current_active_user, get_admin_user, get_tutor_user

router = APIRouter(prefix="/equipos", tags=["equipos"])

@router.get("/", response_model=List[EquipoSchema])
def get_equipos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener todos los equipos"""
    equipos = db.query(Equipo).all()
    return equipos

@router.get("/{equipo_id}", response_model=EquipoSchema)
def get_equipo(
    equipo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener un equipo específico"""
    equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    return equipo

@router.post("/", response_model=EquipoSchema)
def create_equipo(
    equipo: EquipoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Crear un nuevo equipo (solo administradores)"""
    db_equipo = Equipo(**equipo.dict())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

@router.get("/mi-equipo/", response_model=EquipoConDetalles)
def get_mi_equipo(
    db: Session = Depends(get_db),
    current_user = Depends(get_tutor_user)
):
    """Obtener detalles del equipo del tutor actual"""
    if not current_user.equipo_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no tiene equipo asignado"
        )
    
    # Obtener el equipo con sus tutores y colegio
    equipo = db.query(Equipo).filter(Equipo.id == current_user.equipo_id).first()
    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    
    # Obtener tutores del equipo
    tutores = db.query(Tutor).filter(Tutor.equipo_id == equipo.id).all()
    tutores_data = [
        {
            "id": tutor.id,
            "nombre": tutor.nombre,
            "apellido": tutor.apellido,
            "email": tutor.email
        }
        for tutor in tutores
    ]
    
    # Obtener colegio si existe
    colegio_data = None
    if equipo.colegio_id:
        colegio = db.query(Colegio).filter(Colegio.id == equipo.colegio_id).first()
        if colegio:
            colegio_data = {
                "id": colegio.id,
                "nombre": colegio.nombre,
                "comuna": colegio.comuna
            }
    
    # Crear respuesta con detalles
    equipo_data = {
        "id": equipo.id,
        "nombre": equipo.nombre,
        "descripcion": equipo.descripcion,
        "colegio_id": equipo.colegio_id,
        "created_at": equipo.created_at,
        "updated_at": equipo.updated_at,
        "tutores": tutores_data,
        "colegio": colegio_data
    }
    
    return equipo_data
