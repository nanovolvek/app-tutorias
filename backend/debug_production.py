#!/usr/bin/env python3
"""
Script para diagnosticar problemas en producción
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.database import DATABASE_URL

def debug_production():
    """Diagnosticar problemas en producción"""
    
    print("=== DIAGNOSTICO DE PRODUCCION ===")
    
    # 1. Verificar conexión a base de datos
    print("\n1. Verificando conexion a base de datos...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"OK: Conectado a PostgreSQL {version}")
    except Exception as e:
        print(f"ERROR: No se puede conectar a la base de datos: {e}")
        return False
    
    # 2. Verificar tablas existentes
    print("\n2. Verificando tablas existentes...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result]
            print(f"Tablas encontradas: {tables}")
            
            # Verificar tablas específicas
            required_tables = ['estudiantes', 'tutores', 'equipos', 'colegios', 'usuarios']
            missing_tables = [t for t in required_tables if t not in tables]
            if missing_tables:
                print(f"ERROR: Faltan tablas: {missing_tables}")
            else:
                print("OK: Todas las tablas requeridas existen")
                
            # Verificar tablas de asistencia
            attendance_tables = ['asistencia_estudiantes', 'asistencia_tutores']
            missing_attendance = [t for t in attendance_tables if t not in tables]
            if missing_attendance:
                print(f"WARNING: Faltan tablas de asistencia: {missing_attendance}")
            else:
                print("OK: Tablas de asistencia existen")
                
    except Exception as e:
        print(f"ERROR: Error al verificar tablas: {e}")
        return False
    
    # 3. Verificar datos
    print("\n3. Verificando datos...")
    try:
        with engine.connect() as conn:
            # Estudiantes
            result = conn.execute(text("SELECT COUNT(*) FROM estudiantes;"))
            student_count = result.fetchone()[0]
            print(f"Estudiantes: {student_count}")
            
            # Tutores
            result = conn.execute(text("SELECT COUNT(*) FROM tutores;"))
            tutor_count = result.fetchone()[0]
            print(f"Tutores: {tutor_count}")
            
            # Equipos
            result = conn.execute(text("SELECT COUNT(*) FROM equipos;"))
            equipo_count = result.fetchone()[0]
            print(f"Equipos: {equipo_count}")
            
            # Colegios
            result = conn.execute(text("SELECT COUNT(*) FROM colegios;"))
            colegio_count = result.fetchone()[0]
            print(f"Colegios: {colegio_count}")
            
            # Asistencia estudiantes
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM asistencia_estudiantes;"))
                attendance_count = result.fetchone()[0]
                print(f"Asistencia estudiantes: {attendance_count}")
            except:
                print("Asistencia estudiantes: 0 (tabla no existe)")
                
            # Asistencia tutores
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM asistencia_tutores;"))
                attendance_count = result.fetchone()[0]
                print(f"Asistencia tutores: {attendance_count}")
            except:
                print("Asistencia tutores: 0 (tabla no existe)")
                
    except Exception as e:
        print(f"ERROR: Error al verificar datos: {e}")
        return False
    
    # 4. Verificar estructura de tablas
    print("\n4. Verificando estructura de tablas...")
    try:
        with engine.connect() as conn:
            # Verificar estructura de estudiantes
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'estudiantes' 
                ORDER BY ordinal_position;
            """))
            columns = result.fetchall()
            print("Columnas de estudiantes:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
                
    except Exception as e:
        print(f"ERROR: Error al verificar estructura: {e}")
        return False
    
    print("\n=== DIAGNOSTICO COMPLETADO ===")
    return True

if __name__ == "__main__":
    debug_production()
