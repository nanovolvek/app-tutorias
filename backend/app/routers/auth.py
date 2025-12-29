from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import Usuario
from app.schemas.user import (
    UsuarioLogin, Token, Usuario as UsuarioSchema,
    ChangePassword, RequestPasswordReset, ResetPassword
)
from app.auth.security import verify_password, create_access_token, get_password_hash
from app.auth.dependencies import get_current_active_user
from datetime import timedelta, datetime
import secrets
import uuid

router = APIRouter(prefix="/auth", tags=["autenticación"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint para iniciar sesión"""
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "requires_password_change": not user.password_changed
    }

@router.post("/login-json", response_model=Token)
def login_json(user_data: UsuarioLogin, db: Session = Depends(get_db)):
    """Endpoint alternativo para login con JSON"""
    user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "requires_password_change": not user.password_changed
    }

@router.get("/me", response_model=UsuarioSchema)
def get_current_user_info(current_user: Usuario = Depends(get_current_active_user)):
    """Obtener información del usuario actual"""
    return current_user

@router.post("/change-password")
def change_password(
    password_data: ChangePassword,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cambiar la contraseña del usuario actual"""
    # Si el usuario no ha cambiado su contraseña, no requiere la contraseña actual
    if current_user.password_changed:
        # Verificar la contraseña actual solo si ya la ha cambiado antes
        if not verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
    
    # Validar que la nueva contraseña sea diferente
    if verify_password(password_data.new_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe ser diferente a la actual"
        )
    
    # Actualizar la contraseña
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.password_changed = True
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Contraseña actualizada exitosamente"}

@router.post("/request-password-reset")
def request_password_reset(
    reset_data: RequestPasswordReset,
    db: Session = Depends(get_db)
):
    """Solicitar recuperación de contraseña"""
    user = db.query(Usuario).filter(Usuario.email == reset_data.email).first()
    
    # Por seguridad, no revelamos si el email existe o no
    if not user:
        return {"message": "Si el email existe, se enviará un enlace de recuperación"}
    
    # Generar token de recuperación
    reset_token = secrets.token_urlsafe(32)
    user.password_reset_token = reset_token
    user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
    db.commit()
    
    # En un entorno real, aquí enviarías un email con el token
    # Por ahora, retornamos el token (solo para desarrollo)
    # TODO: Implementar envío de email
    return {
        "message": "Si el email existe, se enviará un enlace de recuperación",
        "token": reset_token  # Solo para desarrollo, eliminar en producción
    }

@router.post("/reset-password")
def reset_password(
    reset_data: ResetPassword,
    db: Session = Depends(get_db)
):
    """Resetear contraseña usando token"""
    user = db.query(Usuario).filter(Usuario.password_reset_token == reset_data.token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido"
        )
    
    if user.password_reset_expires and user.password_reset_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expirado"
        )
    
    # Actualizar contraseña
    user.hashed_password = get_password_hash(reset_data.new_password)
    user.password_changed = True
    user.password_reset_token = None
    user.password_reset_expires = None
    db.commit()
    
    return {"message": "Contraseña restablecida exitosamente"}
