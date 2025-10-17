from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.student import Estudiante
from app.models.equipo import Equipo
from app.models.school import Colegio
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
        estudiantes = db.query(Estudiante).options(
            joinedload(Estudiante.equipo).joinedload(Equipo.colegio)
        ).all()
    else:
        # Tutor solo puede ver estudiantes de su equipo
        estudiantes = db.query(Estudiante).options(
            joinedload(Estudiante.equipo).joinedload(Equipo.colegio)
        ).filter(Estudiante.equipo_id == current_user.equipo_id).all()
    
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
    current_user = Depends(get_current_active_user)
):
    """Crear un nuevo estudiante"""
    # Verificar que el equipo existe
    equipo = db.query(Equipo).filter(Equipo.id == estudiante.equipo_id).first()
    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    
    # Si es tutor, verificar que solo puede agregar estudiantes a su equipo
    if current_user.rol == "tutor" and estudiante.equipo_id != current_user.equipo_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes agregar estudiantes a tu equipo"
        )
    
    # Verificar que el RUT no esté en uso
    existing_estudiante = db.query(Estudiante).filter(Estudiante.rut == estudiante.rut).first()
    if existing_estudiante:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un estudiante con este RUT"
        )
    
    try:
        db_estudiante = Estudiante(**estudiante.dict())
        db.add(db_estudiante)
        db.commit()
        db.refresh(db_estudiante)
        return db_estudiante
    except Exception as e:
        db.rollback()
        # Si hay error de ID duplicado, intentar obtener el siguiente ID disponible
        if "llave duplicada" in str(e) or "duplicate key" in str(e):
            # Obtener el máximo ID actual
            max_id = db.query(Estudiante).order_by(Estudiante.id.desc()).first()
            next_id = (max_id.id + 1) if max_id else 1
            
            # Crear el estudiante con ID explícito
            estudiante_data = estudiante.dict()
            db_estudiante = Estudiante(id=next_id, **estudiante_data)
            db.add(db_estudiante)
            db.commit()
            db.refresh(db_estudiante)
            return db_estudiante
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el estudiante: {str(e)}"
            )

@router.delete("/{estudiante_id}")
def delete_estudiante(
    estudiante_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Eliminar un estudiante (eliminación física)"""
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar permisos - tutores solo pueden eliminar estudiantes de su equipo
    if current_user.rol == "tutor" and estudiante.equipo_id != current_user.equipo_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes eliminar estudiantes de tu equipo"
        )
    
    # Eliminar físicamente
    db.delete(estudiante)
    db.commit()
    
    return {"message": "Estudiante eliminado exitosamente"}
