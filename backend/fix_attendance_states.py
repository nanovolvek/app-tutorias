#!/usr/bin/env python3
"""
Script para corregir los estados de asistencia en producción
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def fix_attendance_states():
    """Corregir los estados de asistencia a minúsculas"""
    print("Corrigiendo estados de asistencia en produccion...")
    
    # Configurar URL de producción
    prod_db_url = 'postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres'
    engine = create_engine(prod_db_url)
    
    try:
        with engine.connect() as conn:
            # Actualizar estados en asistencia_estudiantes
            print("Actualizando estados en asistencia_estudiantes...")
            conn.execute(text("""
                UPDATE asistencia_estudiantes 
                SET estado = 'asistio' 
                WHERE estado = 'ASISTIO'
            """))
            
            conn.execute(text("""
                UPDATE asistencia_estudiantes 
                SET estado = 'no_asistio' 
                WHERE estado = 'NO_ASISTIO'
            """))
            
            conn.execute(text("""
                UPDATE asistencia_estudiantes 
                SET estado = 'tutoria_suspendida' 
                WHERE estado = 'SUSPENDIDA'
            """))
            
            conn.execute(text("""
                UPDATE asistencia_estudiantes 
                SET estado = 'vacaciones_feriado' 
                WHERE estado = 'VACACIONES'
            """))
            
            # Actualizar estados en asistencia_tutores
            print("Actualizando estados en asistencia_tutores...")
            conn.execute(text("""
                UPDATE asistencia_tutores 
                SET estado = 'asistio' 
                WHERE estado = 'ASISTIO'
            """))
            
            conn.execute(text("""
                UPDATE asistencia_tutores 
                SET estado = 'no_asistio' 
                WHERE estado = 'NO_ASISTIO'
            """))
            
            conn.execute(text("""
                UPDATE asistencia_tutores 
                SET estado = 'tutoria_suspendida' 
                WHERE estado = 'SUSPENDIDA'
            """))
            
            conn.execute(text("""
                UPDATE asistencia_tutores 
                SET estado = 'vacaciones_feriado' 
                WHERE estado = 'VACACIONES'
            """))
            
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
            print("\nEstados de asistencia corregidos exitosamente!")
            return True
            
    except Exception as e:
        print(f"Error corrigiendo estados: {e}")
        return False

def main():
    """Función principal"""
    print("CORRIGIENDO ESTADOS DE ASISTENCIA EN PRODUCCION")
    print("=" * 60)
    
    success = fix_attendance_states()
    
    if success:
        print("\n" + "=" * 60)
        print("ESTADOS CORREGIDOS EXITOSAMENTE!")
        print("Ahora la aplicacion deberia mostrar correctamente:")
        print("- Graficos de asistencia")
        print("- Porcentajes de asistencia")
        print("- Estadisticas del dashboard")
    else:
        print("\nError corrigiendo estados")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
