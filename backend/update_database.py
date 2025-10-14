#!/usr/bin/env python3
"""
Script para actualizar la base de datos con las nuevas columnas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database import engine

def update_database():
    """Actualizar la base de datos con las nuevas columnas"""
    try:
        with engine.connect() as connection:
            # Agregar las nuevas columnas a la tabla students
            print("Agregando nuevas columnas a la tabla students...")
            
            # Verificar si las columnas ya existen
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'students' AND column_name IN ('rut', 'guardian_name', 'guardian_contact', 'observations')
            """))
            existing_columns = [row[0] for row in result]
            
            # Agregar columnas que no existen
            if 'rut' not in existing_columns:
                print("Agregando columna 'rut'...")
                connection.execute(text("ALTER TABLE students ADD COLUMN rut VARCHAR UNIQUE"))
            
            if 'guardian_name' not in existing_columns:
                print("Agregando columna 'guardian_name'...")
                connection.execute(text("ALTER TABLE students ADD COLUMN guardian_name VARCHAR"))
            
            if 'guardian_contact' not in existing_columns:
                print("Agregando columna 'guardian_contact'...")
                connection.execute(text("ALTER TABLE students ADD COLUMN guardian_contact VARCHAR"))
            
            if 'observations' not in existing_columns:
                print("Agregando columna 'observations'...")
                connection.execute(text("ALTER TABLE students ADD COLUMN observations VARCHAR"))
            
            # Crear tabla attendance si no existe
            print("Creando tabla attendance...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL REFERENCES students(id),
                    week VARCHAR NOT NULL,
                    attended BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """))
            
            connection.commit()
            print("Base de datos actualizada exitosamente!")
            
    except Exception as e:
        print(f"Error actualizando la base de datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = update_database()
    if success:
        print("Actualización completada exitosamente")
    else:
        print("Error en la actualización")
        sys.exit(1)
