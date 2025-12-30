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
from app.utils.email import send_password_reset_email

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
    try:
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
        
        # Manejar caso donde password_changed puede no existir (migración pendiente)
        password_changed = getattr(user, 'password_changed', True)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "requires_password_change": not password_changed
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

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
    import logging
    import os
    import sys
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Log inicial
    logger.info(f"[PASSWORD-RESET] Solicitud de recuperación para: {reset_data.email}")
    print(f"[PASSWORD-RESET] Solicitud de recuperación para: {reset_data.email}", file=sys.stderr)
    
    user = db.query(Usuario).filter(Usuario.email == reset_data.email).first()
    
    # Por seguridad, no revelamos si el email existe o no
    if not user:
        logger.info(f"[PASSWORD-RESET] Email no encontrado: {reset_data.email}")
        return {"message": "Si el email existe, se enviará un enlace de recuperación"}
    
    # Generar token de recuperación
    reset_token = secrets.token_urlsafe(32)
    user.password_reset_token = reset_token
    user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
    db.commit()
    
    logger.info(f"[PASSWORD-RESET] Token generado para usuario: {user.email}")
    print(f"[PASSWORD-RESET] Token generado para usuario: {user.email}", file=sys.stderr)
    
    # Verificar variables SMTP antes de enviar
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    
    logger.info(f"[PASSWORD-RESET] SMTP config: SERVER={smtp_server}, PORT={smtp_port}, USER={smtp_user}, PASSWORD={'***' if smtp_password else 'NO CONFIGURADO'}")
    print(f"[PASSWORD-RESET] SMTP config: SERVER={smtp_server}, PORT={smtp_port}, USER={smtp_user}, PASSWORD={'***' if smtp_password else 'NO CONFIGURADO'}", file=sys.stderr)
    
    # Enviar email con el token
    logger.info(f"[PASSWORD-RESET] Intentando enviar email...")
    print(f"[PASSWORD-RESET] Intentando enviar email...", file=sys.stderr)
    email_sent = send_password_reset_email(user.email, reset_token)
    
    if email_sent:
        logger.info(f"[PASSWORD-RESET] ✅ Email enviado exitosamente a {user.email}")
        print(f"[PASSWORD-RESET] ✅ Email enviado exitosamente a {user.email}", file=sys.stderr)
    else:
        logger.error(f"[PASSWORD-RESET] ❌ Error al enviar email a {user.email}")
        print(f"[PASSWORD-RESET] ❌ Error al enviar email a {user.email}", file=sys.stderr)
    
    # Si el email no se pudo enviar (SMTP no configurado), retornar el token en desarrollo
    # En producción, esto no debería pasar si SMTP está configurado
    response = {
        "message": "Si el email existe, se enviará un enlace de recuperación"
    }
    
    # Solo en desarrollo, si SMTP no está configurado, mostrar el token
    if not email_sent and os.getenv("ENVIRONMENT", "production") == "development":
        response["token"] = reset_token  # Solo para desarrollo
        logger.warning(f"[PASSWORD-RESET] Token devuelto en respuesta (solo desarrollo): {reset_token}")
    
    return response

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
