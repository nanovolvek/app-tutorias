#!/usr/bin/env python3
"""
Script para corregir el enum de AttendanceStatus en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.database import DATABASE_URL

def fix_enum():
    """Corregir el enum de AttendanceStatus"""
    
    print("Corrigiendo enum AttendanceStatus...")
    
    # Crear engine
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Primero, eliminar el enum existente si existe
            print("Eliminando enum existente...")
            conn.execute(text("DROP TYPE IF EXISTS attendancestatus CASCADE;"))
            conn.commit()
            
            # Crear el nuevo enum con los valores correctos
            print("Creando nuevo enum...")
            conn.execute(text("""
                CREATE TYPE attendancestatus AS ENUM (
                    'asistió',
                    'no asistió', 
                    'tutoría suspendida',
                    'vacaciones/feriado'
                );
            """))
            conn.commit()
            
            # Verificar que el enum se creó correctamente
            result = conn.execute(text("""
                SELECT enumlabel 
                FROM pg_enum 
                WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'attendancestatus')
                ORDER BY enumsortorder;
            """))
            
            values = [row[0] for row in result]
            print(f"Valores del enum: {values}")
            
            print("Enum corregido exitosamente!")
            
    except Exception as e:
        print(f"Error al corregir enum: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = fix_enum()
    sys.exit(0 if success else 1)
