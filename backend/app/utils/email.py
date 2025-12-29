"""
Utilidades para envío de emails usando SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

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
        print("⚠️  SMTP no configurado. Variables SMTP_USER y SMTP_PASSWORD requeridas.")
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
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email de recuperación enviado a {email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación SMTP: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {e}")
        return False
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

