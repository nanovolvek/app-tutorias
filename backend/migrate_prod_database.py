#!/usr/bin/env python3
"""
Script de migración para aplicar cambios de base de datos en producción
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def migrate_database():
    """Aplicar migraciones a la base de datos de producción"""
    print("Aplicando migraciones a la base de datos de produccion...")
    
    # Obtener conexión a producción
    prod_db_url = os.getenv('DATABASE_URL')
    if not prod_db_url:
        print("Error: DATABASE_URL no esta configurada")
        return False
    
    engine = create_engine(prod_db_url)
    
    try:
        with engine.connect() as conn:
            # Verificar si las tablas de asistencia existen
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'asistencia_estudiantes'
                );
            """)).scalar()
            
            if not result:
                print("Creando tablas de asistencia...")
                
                # Crear tabla asistencia_estudiantes
                conn.execute(text("""
                    CREATE TABLE asistencia_estudiantes (
                        id SERIAL PRIMARY KEY,
                        estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
                        semana INTEGER NOT NULL,
                        estado VARCHAR(50) NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        UNIQUE(estudiante_id, semana)
                    );
                """))
                
                # Crear tabla asistencia_tutores
                conn.execute(text("""
                    CREATE TABLE asistencia_tutores (
                        id SERIAL PRIMARY KEY,
                        tutor_id INTEGER NOT NULL REFERENCES tutores(id),
                        semana INTEGER NOT NULL,
                        estado VARCHAR(50) NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        UNIQUE(tutor_id, semana)
                    );
                """))
                
                # Crear índices
                conn.execute(text("""
                    CREATE INDEX idx_asistencia_estudiantes_estudiante_id 
                    ON asistencia_estudiantes(estudiante_id);
                """))
                
                conn.execute(text("""
                    CREATE INDEX idx_asistencia_tutores_tutor_id 
                    ON asistencia_tutores(tutor_id);
                """))
                
                print("Tablas de asistencia creadas")
            else:
                print("Tablas de asistencia ya existen")
            
            # Verificar si necesitamos agregar campos a tutores
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'tutores' AND column_name = 'telefono'
            """)).fetchone()
            
            if not result:
                print("Agregando campos adicionales a tutores...")
                
                # Agregar campos opcionales a tutores
                conn.execute(text("""
                    ALTER TABLE tutores 
                    ADD COLUMN telefono VARCHAR(20),
                    ADD COLUMN especialidad VARCHAR(100),
                    ADD COLUMN experiencia_anos INTEGER DEFAULT 0,
                    ADD COLUMN observaciones TEXT;
                """))
                
                print("Campos adicionales agregados a tutores")
            else:
                print("Campos adicionales ya existen en tutores")
            
            # Verificar si necesitamos agregar campo deleted a estudiantes
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'estudiantes' AND column_name = 'deleted'
            """)).fetchone()
            
            if not result:
                print("Agregando campo deleted a estudiantes...")
                
                # Agregar campo deleted a estudiantes
                conn.execute(text("""
                    ALTER TABLE estudiantes 
                    ADD COLUMN deleted BOOLEAN DEFAULT FALSE NOT NULL;
                """))
                
                print("Campo deleted agregado a estudiantes")
            else:
                print("Campo deleted ya existe en estudiantes")
            
            conn.commit()
            print("Migraciones aplicadas exitosamente!")
            return True
            
    except Exception as e:
        print(f"Error durante la migracion: {e}")
        return False

def main():
    """Función principal"""
    print("Iniciando migracion de base de datos de produccion")
    
    # Verificar que estamos en producción
    if not os.getenv('DATABASE_URL') or 'localhost' in os.getenv('DATABASE_URL', ''):
        print("Error: No se detecto configuracion de produccion")
        print("   Asegurate de que DATABASE_URL apunte a la base de datos de produccion")
        return False
    
    success = migrate_database()
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
