"""
Utilidades para envío de emails usando SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_password_reset_email(email: str, token: str) -> bool:
    """
    Envía email de recuperación de contraseña usando SMTP
    
    Args:
        email: Email del destinatario
        token: Token de recuperación de contraseña
        
    Returns:
        True si el email se envió exitosamente, False en caso contrario
    """
    # Configuración SMTP desde variables de entorno
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    frontend_url = os.getenv("FRONTEND_URL", "https://app-tutorias.onrender.com")
    
    # Si no hay configuración SMTP, retornar False
    if not smtp_user or not smtp_password:
        error_msg = "⚠️  SMTP no configurado. Variables SMTP_USER y SMTP_PASSWORD requeridas."
        logger.error(error_msg)
        print(error_msg, file=sys.stderr)
        print(f"[EMAIL] SMTP_USER={smtp_user}, SMTP_PASSWORD={'***' if smtp_password else 'None'}", file=sys.stderr)
        return False
    
    # URL del reset
    reset_url = f"{frontend_url}/reset-password?token={token}"
    
    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "Recuperación de Contraseña - Plataforma Tutorías"
    
    # Cuerpo del email
    body = f"""
Hola,

Has solicitado recuperar tu contraseña en la Plataforma de Tutorías.

Haz clic en el siguiente enlace para restablecer tu contraseña:

{reset_url}

Este enlace expirará en 1 hora por seguridad.

Si no solicitaste este cambio de contraseña, puedes ignorar este email de forma segura.

Saludos,
Equipo Plataforma Tutorías
"""
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Enviar email
    try:
        log_msg = f"[EMAIL] Intentando conectar a {smtp_server}:{smtp_port}..."
        logger.info(log_msg)
        print(log_msg, file=sys.stderr)
        
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        log_msg = "[EMAIL] Conexión establecida, iniciando STARTTLS..."
        logger.info(log_msg)
        print(log_msg, file=sys.stderr)
        
        server.starttls()
        log_msg = f"[EMAIL] Autenticando con usuario: {smtp_user}..."
        logger.info(log_msg)
        print(log_msg, file=sys.stderr)
        
        server.login(smtp_user, smtp_password)
        log_msg = f"[EMAIL] Autenticación exitosa, enviando email a {email}..."
        logger.info(log_msg)
        print(log_msg, file=sys.stderr)
        
        server.send_message(msg)
        server.quit()
        success_msg = f"✅ Email de recuperación enviado a {email}"
        logger.info(success_msg)
        print(success_msg, file=sys.stderr)
        return True
    except smtplib.SMTPConnectError as e:
        error_msg = f"❌ Error de conexión SMTP: No se pudo conectar a {smtp_server}:{smtp_port} - {e}"
        logger.error(error_msg)
        print(error_msg, file=sys.stderr)
        return False
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"❌ Error de autenticación SMTP: {e} - Verifica SMTP_USER y SMTP_PASSWORD"
        logger.error(error_msg)
        print(error_msg, file=sys.stderr)
        return False
    except smtplib.SMTPException as e:
        error_msg = f"❌ Error SMTP: {e}"
        logger.error(error_msg)
        print(error_msg, file=sys.stderr)
        return False
    except Exception as e:
        error_msg = f"❌ Error enviando email: {type(e).__name__}: {e}"
        logger.error(error_msg, exc_info=True)
        print(error_msg, file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return False

