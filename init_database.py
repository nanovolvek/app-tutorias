#!/usr/bin/env python3
"""
Script para inicializar la base de datos en Railway
"""
import os
import sys
sys.path.append('backend')

from sqlalchemy import create_engine, text
from app.models import Base

def init_database():
    """Inicializa la base de datos con tablas y datos de ejemplo"""
    
    print("Iniciando base de datos...")
    
    # Obtener URL de la base de datos desde variables de entorno
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("Error: DATABASE_URL no encontrada en variables de entorno")
        return False
    
    try:
        # Conectar a la base de datos
        print("Conectando a la base de datos...")
        engine = create_engine(DATABASE_URL)
        
        # Crear todas las tablas
        print("Creando tablas...")
        with engine.connect() as conn:
            # Crear todas las tablas usando los modelos
            Base.metadata.create_all(bind=engine)
            print("Tablas creadas exitosamente")
            
            # Verificar si ya hay datos
            result = conn.execute(text("SELECT COUNT(*) FROM schools"))
            school_count = result.scalar()
            
            if school_count == 0:
                print("Insertando datos de ejemplo...")
                
                # Insertar colegio de ejemplo
                conn.execute(text("""
                    INSERT INTO schools (name, address, phone, email, created_at, updated_at) 
                    VALUES ('Colegio Ejemplo', 'Calle Principal 123', '123456789', 'info@colegio.com', NOW(), NOW())
                """))
                
                # Insertar usuario administrador
                conn.execute(text("""
                    INSERT INTO users (email, hashed_password, full_name, is_active, role, created_at, updated_at) 
                    VALUES ('admin@tutorias.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2G', 'Administrador', true, 'admin', NOW(), NOW())
                """))
                
                # Insertar tutor de ejemplo
                conn.execute(text("""
                    INSERT INTO tutors (user_id, school_id, subject, experience_years, created_at, updated_at) 
                    VALUES (1, 1, 'Matemáticas', 5, NOW(), NOW())
                """))
                
                # Insertar estudiante de ejemplo
                conn.execute(text("""
                    INSERT INTO students (name, email, grade, school_id, created_at, updated_at) 
                    VALUES ('Juan Pérez', 'juan@estudiante.com', '10°', 1, NOW(), NOW())
                """))
                
                # Insertar equipo de ejemplo
                conn.execute(text("""
                    INSERT INTO equipos (name, description, school_id, created_at, updated_at) 
                    VALUES ('Equipo Matemáticas', 'Equipo de apoyo en matemáticas', 1, NOW(), NOW())
                """))
                
                conn.commit()
                print("Datos de ejemplo insertados exitosamente")
            else:
                print("La base de datos ya contiene datos, saltando inserción")
        
        print("Base de datos inicializada correctamente!")
        return True
        
    except Exception as e:
        print(f"Error inicializando la base de datos: {e}")
        return False
    
    finally:
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
    init_database()
