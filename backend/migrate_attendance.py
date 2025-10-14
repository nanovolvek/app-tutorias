#!/usr/bin/env python3
"""
Script para migrar la base de datos y crear las nuevas tablas de asistencia
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.database import get_db
from app.models import Base
from app.database import DATABASE_URL

def migrate_database():
    """Crear las nuevas tablas de asistencia"""
    
    print("Iniciando migracion de la base de datos...")
    
    # Crear engine
    engine = create_engine(DATABASE_URL)
    
    try:
        # Crear las nuevas tablas
        print("Creando nuevas tablas de asistencia...")
        Base.metadata.create_all(bind=engine)
        print("Nuevas tablas creadas exitosamente")
        
        # Verificar que las tablas existen
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('student_attendance', 'tutor_attendance')
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result]
            print(f"Tablas creadas: {', '.join(tables)}")
            
            if 'student_attendance' in tables and 'tutor_attendance' in tables:
                print("Migracion completada exitosamente!")
                print("\nProximos pasos:")
                print("1. Ejecutar el backend: python -m uvicorn app.main:app --reload")
                print("2. Ejecutar el frontend: npm run dev")
                print("3. Probar la nueva funcionalidad de asistencia")
            else:
                print("Error: No se pudieron crear todas las tablas")
                
    except Exception as e:
        print(f"Error durante la migracion: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
