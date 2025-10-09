from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.school import School
from app.schemas.school import School as SchoolSchema, SchoolCreate, SchoolUpdate
from app.auth.dependencies import get_current_active_user, get_admin_user
from app.models.user import User

router = APIRouter(prefix="/schools", tags=["colegios"])

@router.get("/", response_model=List[SchoolSchema])
def get_schools(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener lista de colegios"""
    schools = db.query(School).offset(skip).limit(limit).all()
    return schools

@router.get("/{school_id}", response_model=SchoolSchema)
def get_school(
    school_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un colegio por ID"""
    school = db.query(School).filter(School.id == school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    return school

@router.post("/", response_model=SchoolSchema)
def create_school(
    school: SchoolCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Crear un nuevo colegio (solo administradores)"""
    db_school = School(**school.dict())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

@router.put("/{school_id}", response_model=SchoolSchema)
def update_school(
    school_id: int, 
    school: SchoolUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Actualizar un colegio (solo administradores)"""
    db_school = db.query(School).filter(School.id == school_id).first()
    if db_school is None:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    update_data = school.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_school, field, value)
    
    db.commit()
    db.refresh(db_school)
    return db_school

@router.delete("/{school_id}")
def delete_school(
    school_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Eliminar un colegio (solo administradores)"""
    db_school = db.query(School).filter(School.id == school_id).first()
    if db_school is None:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    db.delete(db_school)
    db.commit()
    return {"message": "Colegio eliminado correctamente"}
