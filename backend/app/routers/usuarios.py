from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import Usuario
from app.models.equipo import Equipo
from app.schemas.user import Usuario as UsuarioSchema, UsuarioCreate
from app.auth.dependencies import get_current_active_user, get_admin_user
from app.auth.security import get_password_hash

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=List[UsuarioSchema])
def get_usuarios(
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Obtener todos los usuarios (solo administradores)"""
    usuarios = db.query(Usuario).all()
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioSchema)
def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Obtener un usuario específico (solo administradores)"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.post("/", response_model=UsuarioSchema)
def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Crear un nuevo usuario (solo administradores)"""
    # Verificar que el equipo existe si es un tutor
    if usuario.rol == "tutor" and usuario.equipo_id:
        equipo = db.query(Equipo).filter(Equipo.id == usuario.equipo_id).first()
        if not equipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipo no encontrado"
            )
    
    # Verificar que el email no esté en uso
    existing_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está en uso"
        )
    
    # Crear el usuario
    usuario_data = usuario.dict()
    usuario_data["hashed_password"] = get_password_hash(usuario_data.pop("password"))
    usuario_data["password_changed"] = False  # El usuario debe cambiar su contraseña al primer login
    
    db_usuario = Usuario(**usuario_data)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/me/info", response_model=UsuarioSchema)
def get_my_info(
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener información del usuario actual"""
    return current_user
