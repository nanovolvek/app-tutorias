"""
Script para inicializar la base de datos en Supabase
Ejecutar: python init_supabase.py
"""
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env.production')

# Verificar que DATABASE_URL esté configurada
if not os.getenv('DATABASE_URL'):
    print("❌ Error: DATABASE_URL no está configurada en .env.production")
    print("Por favor, configura las credenciales de Supabase en .env.production")
    sys.exit(1)

# Importar después de configurar las variables de entorno
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.auth.security import get_password_hash

def init_supabase_db():
    """Inicializa la base de datos en Supabase con datos de ejemplo"""
    print("🚀 Inicializando base de datos en Supabase...")
    
    # Crear las tablas
    print("📋 Creando tablas...")
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existen datos
        if db.query(models.Usuario).first():
            print("⚠️  La base de datos ya tiene datos. Saltando inicialización.")
            return
        
        print("👥 Creando equipos...")
        # Crear equipos A, B, C
        equipos_data = [
            {"nombre": "A", "descripcion": "Equipo A - Tutores de Matemáticas"},
            {"nombre": "B", "descripcion": "Equipo B - Tutores de Lenguaje"},
            {"nombre": "C", "descripcion": "Equipo C - Tutores de Ciencias"}
        ]
        
        equipos = []
        for equipo_data in equipos_data:
            equipo = models.Equipo(**equipo_data)
            db.add(equipo)
            equipos.append(equipo)
        
        db.commit()
        
        # Refrescar para obtener los IDs
        for equipo in equipos:
            db.refresh(equipo)
        
        print("👤 Creando usuarios...")
        # Crear usuarios de ejemplo
        usuarios_data = [
            {
                "email": "admin@tutorias.com",
                "hashed_password": get_password_hash("admin123"),
                "nombre_completo": "Administrador Sistema",
                "rol": "admin",
                "equipo_id": None
            },
            {
                "email": "tutor1@tutorias.com",
                "hashed_password": get_password_hash("tutor123"),
                "nombre_completo": "María González",
                "rol": "tutor",
                "equipo_id": equipos[0].id  # Equipo A
            },
            {
                "email": "tutor2@tutorias.com",
                "hashed_password": get_password_hash("tutor123"),
                "nombre_completo": "Carlos Rodríguez",
                "rol": "tutor",
                "equipo_id": equipos[1].id  # Equipo B
            }
        ]
        
        usuarios = []
        for usuario_data in usuarios_data:
            usuario = models.Usuario(**usuario_data)
            db.add(usuario)
            usuarios.append(usuario)
        
        db.commit()
        
        # Refrescar para obtener los IDs
        for usuario in usuarios:
            db.refresh(usuario)
        
        print("👨‍🏫 Creando tutores...")
        # Crear tutores de ejemplo
        tutores_data = [
            {
                "nombre": "María",
                "apellido": "González",
                "email": "maria.gonzalez@email.com",
                "equipo_id": equipos[0].id  # Equipo A
            },
            {
                "nombre": "Carlos",
                "apellido": "Rodríguez",
                "email": "carlos.rodriguez@email.com",
                "equipo_id": equipos[1].id  # Equipo B
            },
            {
                "nombre": "Ana",
                "apellido": "Martínez",
                "email": "ana.martinez@email.com",
                "equipo_id": equipos[0].id  # Equipo A
            },
            {
                "nombre": "Pedro",
                "apellido": "Silva",
                "email": "pedro.silva@email.com",
                "equipo_id": equipos[1].id  # Equipo B
            },
            {
                "nombre": "Laura",
                "apellido": "López",
                "email": "laura.lopez@email.com",
                "equipo_id": equipos[2].id  # Equipo C
            },
            {
                "nombre": "Diego",
                "apellido": "Fernández",
                "email": "diego.fernandez@email.com",
                "equipo_id": equipos[2].id  # Equipo C
            }
        ]
        
        tutores = []
        for tutor_data in tutores_data:
            tutor = models.Tutor(**tutor_data)
            db.add(tutor)
            tutores.append(tutor)
        
        db.commit()
        
        # Refrescar para obtener los IDs
        for tutor in tutores:
            db.refresh(tutor)
        
        print("🎓 Creando estudiantes...")
        # Crear estudiantes de ejemplo (5 por equipo)
        estudiantes_data = [
            # Equipo A
            {"rut": "12.345.678-9", "nombre": "Ana", "apellido": "Silva", "curso": "3° Básico", "equipo_id": equipos[0].id},
            {"rut": "23.456.789-0", "nombre": "Diego", "apellido": "Martínez", "curso": "4° Básico", "equipo_id": equipos[0].id},
            {"rut": "34.567.890-1", "nombre": "Sofía", "apellido": "López", "curso": "5° Básico", "equipo_id": equipos[0].id},
            {"rut": "45.678.901-2", "nombre": "Mateo", "apellido": "García", "curso": "6° Básico", "equipo_id": equipos[0].id},
            {"rut": "56.789.012-3", "nombre": "Valentina", "apellido": "Hernández", "curso": "7° Básico", "equipo_id": equipos[0].id},
            
            # Equipo B
            {"rut": "67.890.123-4", "nombre": "Sebastián", "apellido": "Torres", "curso": "1° Medio", "equipo_id": equipos[1].id},
            {"rut": "78.901.234-5", "nombre": "Isabella", "apellido": "Vargas", "curso": "2° Medio", "equipo_id": equipos[1].id},
            {"rut": "89.012.345-6", "nombre": "Nicolás", "apellido": "Morales", "curso": "3° Medio", "equipo_id": equipos[1].id},
            {"rut": "90.123.456-7", "nombre": "Camila", "apellido": "Rojas", "curso": "4° Medio", "equipo_id": equipos[1].id},
            {"rut": "01.234.567-8", "nombre": "Andrés", "apellido": "Jiménez", "curso": "1° Medio", "equipo_id": equipos[1].id},
            
            # Equipo C
            {"rut": "11.234.567-9", "nombre": "Emilia", "apellido": "Castro", "curso": "2° Básico", "equipo_id": equipos[2].id},
            {"rut": "22.345.678-0", "nombre": "Maximiliano", "apellido": "Ruiz", "curso": "3° Básico", "equipo_id": equipos[2].id},
            {"rut": "33.456.789-1", "nombre": "Antonella", "apellido": "Díaz", "curso": "4° Básico", "equipo_id": equipos[2].id},
            {"rut": "44.567.890-2", "nombre": "Benjamín", "apellido": "Moreno", "curso": "5° Básico", "equipo_id": equipos[2].id},
            {"rut": "55.678.901-3", "nombre": "Javiera", "apellido": "Pérez", "curso": "6° Básico", "equipo_id": equipos[2].id}
        ]
        
        estudiantes = []
        for estudiante_data in estudiantes_data:
            estudiante = models.Estudiante(**estudiante_data)
            db.add(estudiante)
            estudiantes.append(estudiante)
        
        db.commit()
        
        print("✅ Base de datos inicializada correctamente en Supabase!")
        print(f"   - 3 equipos (A, B, C)")
        print(f"   - 3 usuarios (1 admin, 2 tutores)")
        print(f"   - 6 tutores (2 por equipo)")
        print(f"   - 15 estudiantes (5 por equipo)")
        print("\n🔑 Credenciales de acceso:")
        print("   Admin: admin@tutorias.com / admin123")
        print("   Tutor Equipo A: tutor1@tutorias.com / tutor123")
        print("   Tutor Equipo B: tutor2@tutorias.com / tutor123")
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_supabase_db()
