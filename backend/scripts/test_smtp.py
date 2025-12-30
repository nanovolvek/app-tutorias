"""
Script de diagnóstico para probar la configuración SMTP
"""
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_smtp_connection():
    """Prueba la conexión SMTP con las variables configuradas"""
    
    print("=" * 60)
    print("  Diagnostico de Configuracion SMTP")
    print("=" * 60)
    print()
    
    # Obtener variables de entorno
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    frontend_url = os.getenv("FRONTEND_URL", "https://app-tutorias.onrender.com")
    
    print("[*] Verificando variables de entorno...")
    print(f"    SMTP_SERVER: {smtp_server or 'NO CONFIGURADO'}")
    print(f"    SMTP_PORT: {smtp_port or 'NO CONFIGURADO'}")
    print(f"    SMTP_USER: {smtp_user or 'NO CONFIGURADO'}")
    print(f"    SMTP_PASSWORD: {'*' * len(smtp_password) if smtp_password else 'NO CONFIGURADO'}")
    print(f"    FRONTEND_URL: {frontend_url}")
    print()
    
    # Verificar que todas las variables estén configuradas
    if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
        print("[ERROR] Faltan variables de entorno requeridas!")
        print("        Configura SMTP_SERVER, SMTP_PORT, SMTP_USER y SMTP_PASSWORD")
        return False
    
    # Convertir puerto a entero
    try:
        smtp_port = int(smtp_port)
    except ValueError:
        print(f"[ERROR] SMTP_PORT debe ser un numero, recibido: {smtp_port}")
        return False
    
    # Probar conexión SMTP
    print(f"[*] Intentando conectar a {smtp_server}:{smtp_port}...")
    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        print("[OK] Conexion al servidor SMTP exitosa")
    except smtplib.SMTPConnectError as e:
        print(f"[ERROR] No se pudo conectar al servidor SMTP: {e}")
        print(f"        Verifica que SMTP_SERVER y SMTP_PORT sean correctos")
        return False
    except Exception as e:
        print(f"[ERROR] Error de conexion: {e}")
        return False
    
    # Probar STARTTLS
    print("[*] Iniciando STARTTLS...")
    try:
        server.starttls()
        print("[OK] STARTTLS iniciado correctamente")
    except Exception as e:
        print(f"[ERROR] Error al iniciar STARTTLS: {e}")
        print(f"        Si usas puerto 465, deberias usar SSL directo en lugar de STARTTLS")
        server.quit()
        return False
    
    # Probar autenticación
    print(f"[*] Autenticando con usuario: {smtp_user}...")
    try:
        server.login(smtp_user, smtp_password)
        print("[OK] Autenticacion exitosa")
    except smtplib.SMTPAuthenticationError as e:
        print(f"[ERROR] Error de autenticacion: {e}")
        print(f"        Verifica que SMTP_USER y SMTP_PASSWORD sean correctos")
        print(f"        Si usas Gmail, asegurate de usar una App Password, no tu contraseña normal")
        server.quit()
        return False
    except Exception as e:
        print(f"[ERROR] Error al autenticar: {e}")
        server.quit()
        return False
    
    # Probar envío de email de prueba
    test_email = input("\n[*] Ingresa un email de prueba para enviar (o Enter para saltar): ").strip()
    
    if test_email:
        print(f"[*] Enviando email de prueba a {test_email}...")
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = test_email
            msg['Subject'] = "Prueba SMTP - Plataforma Tutorias"
            
            body = """
Este es un email de prueba para verificar la configuracion SMTP.

Si recibes este email, la configuracion SMTP esta funcionando correctamente.
"""
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            server.send_message(msg)
            print(f"[OK] Email de prueba enviado exitosamente a {test_email}")
            print(f"     Revisa tu bandeja de entrada (y spam)")
        except Exception as e:
            print(f"[ERROR] Error al enviar email: {e}")
            server.quit()
            return False
    
    server.quit()
    print("\n[OK] Diagnostico completado exitosamente!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        test_smtp_connection()
    except KeyboardInterrupt:
        print("\n[!] Diagnostico cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

