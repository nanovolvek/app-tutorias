from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.equipo import Equipo
from app.schemas.equipo import Equipo as EquipoSchema, EquipoCreate
from app.auth.dependencies import get_current_active_user, get_admin_user

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
