"""
Script para inicializar la base de datos con datos de ejemplo
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.auth.security import get_password_hash

# Crear las tablas
models.Base.metadata.create_all(bind=engine)

def init_db():
    """Inicializa la base de datos con datos de ejemplo"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existen datos
        if db.query(models.Usuario).first():
            print("La base de datos ya tiene datos. Saltando inicialización.")
            return
        
        # Crear usuarios de ejemplo
        admin_user = models.Usuario(
            email="admin@tutorias.com",
            hashed_password=get_password_hash("admin"),
            nombre_completo="Administrador Sistema",
            rol="admin",
            is_active=True
        )
        
        tutor_user = models.Usuario(
            email="tutor@tutorias.com",
            hashed_password=get_password_hash("tutor"),
            nombre_completo="Tutor Equipo A",
            rol="tutor",
            is_active=True
        )
        
        db.add(admin_user)
        db.add(tutor_user)
        
        # Crear colegios de ejemplo
        colegio1 = models.Colegio(
            nombre="Colegio San Patricio",
            comuna="Las Condes"
        )
        
        colegio2 = models.Colegio(
            nombre="Liceo Manuel Barros Borgoño",
            comuna="Santiago"
        )
        
        db.add(colegio1)
        db.add(colegio2)
        db.commit()
        
        # Refrescar para obtener los IDs
        db.refresh(colegio1)
        db.refresh(colegio2)
        
        # Crear equipos de ejemplo
        equipo1 = models.Equipo(
            nombre="Equipo 1",
            descripcion="Equipo de tutores para Colegio San Patricio",
            colegio_id=colegio1.id
        )
        
        equipo2 = models.Equipo(
            nombre="Equipo 2",
            descripcion="Equipo de tutores para Liceo Manuel Barros Borgoño",
            colegio_id=colegio2.id
        )
        
        db.add(equipo1)
        db.add(equipo2)
        db.commit()
        
        # Refrescar para obtener los IDs
        db.refresh(equipo1)
        db.refresh(equipo2)
        
        # Asignar equipo al tutor
        tutor_user.equipo_id = equipo1.id
        
        # Crear tutores de ejemplo
        tutor1 = models.Tutor(
            nombre="Ana",
            apellido="Garcia",
            email="ana.garcia@email.com",
            equipo_id=equipo1.id
        )
        
        tutor2 = models.Tutor(
            nombre="Carlos",
            apellido="Lopez",
            email="carlos.lopez@email.com",
            equipo_id=equipo1.id
        )
        
        db.add(tutor1)
        db.add(tutor2)
        
        # Crear estudiantes de ejemplo
        estudiante1 = models.Estudiante(
            rut="12.345.678-9",
            nombre="Sofia",
            apellido="Silva",
            curso="3° Basico",
            equipo_id=equipo1.id
        )
        
        estudiante2 = models.Estudiante(
            rut="98.765.432-1",
            nombre="Mateo",
            apellido="Gonzalez",
            curso="3° Basico",
            equipo_id=equipo1.id
        )
        
        estudiante3 = models.Estudiante(
            rut="11.222.333-4",
            nombre="Isabella",
            apellido="Perez",
            curso="4° Basico",
            equipo_id=equipo1.id
        )
        
        estudiante4 = models.Estudiante(
            rut="55.666.777-8",
            nombre="Santiago",
            apellido="Hernandez",
            curso="4° Basico",
            equipo_id=equipo1.id
        )
        
        estudiante5 = models.Estudiante(
            rut="99.888.777-6",
            nombre="Valentina",
            apellido="Torres",
            curso="5° Basico",
            equipo_id=equipo1.id
        )
        
        db.add(estudiante1)
        db.add(estudiante2)
        db.add(estudiante3)
        db.add(estudiante4)
        db.add(estudiante5)
        
        db.commit()
        
        print("Base de datos inicializada correctamente con datos de ejemplo:")
        print("   - 2 usuarios (admin@tutorias.com / tutor@tutorias.com)")
        print("   - 2 colegios")
        print("   - 2 equipos")
        print("   - 2 tutores")
        print("   - 5 estudiantes")
        print("\nCredenciales de acceso:")
        print("   Admin: admin@tutorias.com / admin")
        print("   Tutor: tutor@tutorias.com / tutor")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
