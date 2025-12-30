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
    
    try:
        db_usuario = Usuario(**usuario_data)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except Exception as e:
        db.rollback()
        # Si hay error de ID duplicado, obtener el siguiente ID disponible
        if "llave duplicada" in str(e).lower() or "duplicate key" in str(e).lower():
            # Obtener el máximo ID actual
            max_id_result = db.query(Usuario.id).order_by(Usuario.id.desc()).first()
            next_id = (max_id_result[0] + 1) if max_id_result else 1
            
            # Verificar que el ID no exista
            while db.query(Usuario).filter(Usuario.id == next_id).first():
                next_id += 1
            
            # Crear el usuario con ID explícito
            db_usuario = Usuario(id=next_id, **usuario_data)
            db.add(db_usuario)
            db.commit()
            db.refresh(db_usuario)
            return db_usuario
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el usuario: {str(e)}"
            )

@router.get("/me/info", response_model=UsuarioSchema)
def get_my_info(
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener información del usuario actual"""
    return current_user
