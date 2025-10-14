#!/usr/bin/env python3
"""
Script para recrear las tablas con el enum corregido
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.database import DATABASE_URL
from app.models import Base

def recreate_tables():
    """Recrear las tablas con el enum corregido"""
    
    print("Recreando tablas con enum corregido...")
    
    # Crear engine
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Eliminar las tablas existentes
            print("Eliminando tablas existentes...")
            conn.execute(text("DROP TABLE IF EXISTS student_attendance CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS tutor_attendance CASCADE;"))
            conn.commit()
            
        # Recrear las tablas
        print("Recreando tablas...")
        Base.metadata.create_all(bind=engine)
        
        # Verificar que las tablas se crearon
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('student_attendance', 'tutor_attendance')
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result]
            print(f"Tablas recreadas: {', '.join(tables)}")
            
            if 'student_attendance' in tables and 'tutor_attendance' in tables:
                print("Tablas recreadas exitosamente!")
            else:
                print("Error: No se pudieron recrear todas las tablas")
                return False
                
    except Exception as e:
        print(f"Error al recrear tablas: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = recreate_tables()
    sys.exit(0 if success else 1)
