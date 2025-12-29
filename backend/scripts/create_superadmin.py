"""
Script para crear un usuario superadmin
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import Usuario
from app.auth.security import get_password_hash

# Cargar variables de entorno
load_dotenv()

def get_database_url():
    """Obtiene la URL de la base de datos desde variables de entorno"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        db_user = os.getenv("DB_USER", "tutorias_db_user")
        db_password = os.getenv("DB_PASSWORD", "kDL6FlvxRo9urc0X7DHUi86RHi0F2ec2")
        db_host = os.getenv("DB_HOST", "dpg-d3pr88c9c44c73c9snsg-a.oregon-postgres.render.com")
        db_name = os.getenv("DB_NAME", "tutorias_db")
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    
    return database_url

def create_superadmin():
    """Crea un usuario superadmin"""
    
    email = "juanfernandomir@gmail.com"
    nombre_completo = "Juan Fernando Mir"
    password = "Admin123!"  # Contraseña temporal, el usuario deberá cambiarla
    
    database_url = get_database_url()
    
    print("=" * 60)
    print("  Crear Usuario Superadmin")
    print("=" * 60)
    print()
    print(f"[*] Conectando a la base de datos...")
    print(f"    URL: {database_url.split('@')[0]}@***")
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Verificar si el usuario ya existe
        existing_user = session.query(Usuario).filter(Usuario.email == email).first()
        
        if existing_user:
            print(f"\n[!] El usuario con email {email} ya existe.")
            print(f"    ID: {existing_user.id}")
            print(f"    Nombre: {existing_user.nombre_completo}")
            print(f"    Rol: {existing_user.rol}")
            print(f"    Password Changed: {existing_user.password_changed}")
            
            # Actualizar directamente sin preguntar
            existing_user.rol = "admin"
            existing_user.nombre_completo = nombre_completo
            existing_user.hashed_password = get_password_hash(password)
            existing_user.password_changed = False  # Debe cambiar la contraseña
            existing_user.is_active = True
            session.commit()
            print(f"\n[OK] Usuario actualizado a superadmin exitosamente!")
            print(f"    Email: {email}")
            print(f"    Contraseña temporal: {password}")
            print(f"    [IMPORTANTE] El usuario debe cambiar su contraseña al primer login")
            session.close()
            return
        
        else:
            # Crear nuevo usuario
            new_user = Usuario(
                email=email,
                nombre_completo=nombre_completo,
                rol="admin",
                hashed_password=get_password_hash(password),
                password_changed=False,  # Debe cambiar la contraseña al primer login
                is_active=True,
                equipo_id=None
            )
            
            session.add(new_user)
            session.commit()
            
            print(f"\n[OK] Usuario superadmin creado exitosamente!")
            print(f"    Email: {email}")
            print(f"    Nombre: {nombre_completo}")
            print(f"    Rol: admin")
            print(f"    Contraseña temporal: {password}")
            print(f"    [IMPORTANTE] El usuario debe cambiar su contraseña al primer login")
        
        session.close()
        
    except Exception as e:
        print(f"\n[ERROR] Error al crear usuario: {str(e)}")
        sys.exit(1)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    create_superadmin()

