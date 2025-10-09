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
        if db.query(models.User).first():
            print("La base de datos ya tiene datos. Saltando inicialización.")
            return
        
        # Crear usuarios de ejemplo
        admin_user = models.User(
            email="admin@tutorias.com",
            hashed_password=get_password_hash("admin"),
            full_name="Administrador Sistema",
            role="admin",
            is_active=True
        )
        
        tutor_user = models.User(
            email="tutor@tutorias.com",
            hashed_password=get_password_hash("tutor"),
            full_name="Tutor Ejemplo",
            role="tutor",
            is_active=True
        )
        
        db.add(admin_user)
        db.add(tutor_user)
        
        # Crear colegios de ejemplo
        school1 = models.School(
            name="Colegio San Patricio",
            comuna="Las Condes"
        )
        
        school2 = models.School(
            name="Liceo Manuel Barros Borgoño",
            comuna="Santiago"
        )
        
        db.add(school1)
        db.add(school2)
        db.commit()
        
        # Refrescar para obtener los IDs
        db.refresh(school1)
        db.refresh(school2)
        
        # Crear tutores de ejemplo
        tutor1 = models.Tutor(
            first_name="María",
            last_name="González",
            email="maria.gonzalez@email.com",
            school_id=school1.id
        )
        
        tutor2 = models.Tutor(
            first_name="Carlos",
            last_name="Rodríguez",
            email="carlos.rodriguez@email.com",
            school_id=school2.id
        )
        
        db.add(tutor1)
        db.add(tutor2)
        
        # Crear estudiantes de ejemplo
        student1 = models.Student(
            first_name="Ana",
            last_name="Silva",
            course="3° Básico",
            school_id=school1.id
        )
        
        student2 = models.Student(
            first_name="Diego",
            last_name="Martínez",
            course="1° Medio",
            school_id=school2.id
        )
        
        student3 = models.Student(
            first_name="Sofía",
            last_name="López",
            course="5° Básico",
            school_id=school1.id
        )
        
        db.add(student1)
        db.add(student2)
        db.add(student3)
        
        db.commit()
        
        print("Base de datos inicializada correctamente con datos de ejemplo:")
        print("   - 2 usuarios (admin@tutorias.com / tutor@tutorias.com)")
        print("   - 2 colegios")
        print("   - 2 tutores")
        print("   - 3 estudiantes")
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
