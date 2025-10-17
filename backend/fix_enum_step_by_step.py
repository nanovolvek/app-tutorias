#!/usr/bin/env python3
"""
Script para corregir el enum paso a paso
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def fix_enum_step_by_step():
    """Corregir el enum paso a paso"""
    print("Corrigiendo enum paso a paso...")
    
    # Configurar URL de producción
    prod_db_url = 'postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres'
    engine = create_engine(prod_db_url)
    
    try:
        with engine.connect() as conn:
            # Paso 1: Crear tabla temporal con los datos convertidos
            print("Paso 1: Creando tabla temporal...")
            conn.execute(text("""
                CREATE TEMP TABLE temp_asistencia_estudiantes AS
                SELECT id, estudiante_id, semana,
                       CASE estado
                           WHEN 'ASISTIO' THEN 'asistio'
                           WHEN 'NO_ASISTIO' THEN 'no_asistio'
                           WHEN 'SUSPENDIDA' THEN 'tutoria_suspendida'
                           WHEN 'VACACIONES' THEN 'vacaciones_feriado'
                       END as estado,
                       created_at, updated_at
                FROM asistencia_estudiantes
            """))
            
            conn.execute(text("""
                CREATE TEMP TABLE temp_asistencia_tutores AS
                SELECT id, tutor_id, semana,
                       CASE estado
                           WHEN 'ASISTIO' THEN 'asistio'
                           WHEN 'NO_ASISTIO' THEN 'no_asistio'
                           WHEN 'SUSPENDIDA' THEN 'tutoria_suspendida'
                           WHEN 'VACACIONES' THEN 'vacaciones_feriado'
                       END as estado,
                       created_at, updated_at
                FROM asistencia_tutores
            """))
            
            # Paso 2: Crear nuevo enum
            print("Paso 2: Creando nuevo enum...")
            conn.execute(text("""
                CREATE TYPE estadoasistencia_new AS ENUM (
                    'asistio',
                    'no_asistio', 
                    'tutoria_suspendida',
                    'vacaciones_feriado'
                )
            """))
            
            # Paso 3: Cambiar las columnas a VARCHAR temporalmente
            print("Paso 3: Cambiando columnas a VARCHAR...")
            conn.execute(text("""
                ALTER TABLE asistencia_estudiantes 
                ALTER COLUMN estado TYPE VARCHAR(50)
            """))
            
            conn.execute(text("""
                ALTER TABLE asistencia_tutores 
                ALTER COLUMN estado TYPE VARCHAR(50)
            """))
            
            # Paso 4: Actualizar los datos
            print("Paso 4: Actualizando datos...")
            conn.execute(text("""
                UPDATE asistencia_estudiantes 
                SET estado = CASE estado
                    WHEN 'ASISTIO' THEN 'asistio'
                    WHEN 'NO_ASISTIO' THEN 'no_asistio'
                    WHEN 'SUSPENDIDA' THEN 'tutoria_suspendida'
                    WHEN 'VACACIONES' THEN 'vacaciones_feriado'
                END
            """))
            
            conn.execute(text("""
                UPDATE asistencia_tutores 
                SET estado = CASE estado
                    WHEN 'ASISTIO' THEN 'asistio'
                    WHEN 'NO_ASISTIO' THEN 'no_asistio'
                    WHEN 'SUSPENDIDA' THEN 'tutoria_suspendida'
                    WHEN 'VACACIONES' THEN 'vacaciones_feriado'
                END
            """))
            
            # Paso 5: Cambiar las columnas al nuevo enum
            print("Paso 5: Cambiando columnas al nuevo enum...")
            conn.execute(text("""
                ALTER TABLE asistencia_estudiantes 
                ALTER COLUMN estado TYPE estadoasistencia_new 
                USING estado::estadoasistencia_new
            """))
            
            conn.execute(text("""
                ALTER TABLE asistencia_tutores 
                ALTER COLUMN estado TYPE estadoasistencia_new 
                USING estado::estadoasistencia_new
            """))
            
            # Paso 6: Eliminar el enum viejo y renombrar el nuevo
            print("Paso 6: Eliminando enum viejo...")
            conn.execute(text("DROP TYPE estadoasistencia"))
            
            print("Renombrando enum nuevo...")
            conn.execute(text("ALTER TYPE estadoasistencia_new RENAME TO estadoasistencia"))
            
            # Verificar los cambios
            print("\nVerificando cambios en asistencia_estudiantes:")
            estados_estudiantes = conn.execute(text("""
                SELECT DISTINCT estado, COUNT(*) as cantidad
                FROM asistencia_estudiantes
                GROUP BY estado
                ORDER BY estado
            """)).fetchall()
            
            for estado in estados_estudiantes:
                print(f"  '{estado[0]}': {estado[1]} registros")
            
            print("\nVerificando cambios en asistencia_tutores:")
            estados_tutores = conn.execute(text("""
                SELECT DISTINCT estado, COUNT(*) as cantidad
                FROM asistencia_tutores
                GROUP BY estado
                ORDER BY estado
            """)).fetchall()
            
            for estado in estados_tutores:
                print(f"  '{estado[0]}': {estado[1]} registros")
            
            # Calcular porcentajes de muestra
            print("\nCalculando porcentajes de asistencia de muestra:")
            porcentajes = conn.execute(text("""
                SELECT e.nombre, e.apellido,
                       COUNT(ae.id) as total_semanas,
                       COUNT(CASE WHEN ae.estado = 'asistio' THEN 1 END) as semanas_asistio,
                       ROUND(
                           (COUNT(CASE WHEN ae.estado = 'asistio' THEN 1 END)::float / NULLIF(COUNT(ae.id), 0)) * 100, 2
                       ) as porcentaje_asistencia
                FROM estudiantes e
                LEFT JOIN asistencia_estudiantes ae ON e.id = ae.estudiante_id
                GROUP BY e.id, e.nombre, e.apellido
                ORDER BY e.id
                LIMIT 5
            """)).fetchall()
            
            for p in porcentajes:
                print(f"  {p[0]} {p[1]}: {p[3]}/{p[2]} = {p[4]}%")
            
            conn.commit()
            print("\nEnum corregido exitosamente!")
            return True
            
    except Exception as e:
        print(f"Error corrigiendo enum: {e}")
        return False

def main():
    """Función principal"""
    print("CORRIGIENDO ENUM ESTADOASISTENCIA PASO A PASO")
    print("=" * 60)
    
    success = fix_enum_step_by_step()
    
    if success:
        print("\n" + "=" * 60)
        print("ENUM CORREGIDO EXITOSAMENTE!")
        print("Ahora la aplicacion deberia mostrar correctamente:")
        print("- Graficos de asistencia")
        print("- Porcentajes de asistencia")
        print("- Estadisticas del dashboard")
    else:
        print("\nError corrigiendo enum")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
