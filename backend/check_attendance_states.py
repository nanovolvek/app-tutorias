#!/usr/bin/env python3
"""
Script para verificar los estados de asistencia en producción
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def check_attendance_states():
    """Verificar los estados de asistencia"""
    print("Verificando estados de asistencia en produccion...")
    
    # Configurar URL de producción
    prod_db_url = 'postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres'
    engine = create_engine(prod_db_url)
    
    try:
        with engine.connect() as conn:
            # Verificar estados únicos en asistencia_estudiantes
            print("Estados en asistencia_estudiantes:")
            estados_estudiantes = conn.execute(text("""
                SELECT DISTINCT estado, COUNT(*) as cantidad
                FROM asistencia_estudiantes
                GROUP BY estado
                ORDER BY estado
            """)).fetchall()
            
            for estado in estados_estudiantes:
                print(f"  '{estado[0]}': {estado[1]} registros")
            
            # Verificar estados únicos en asistencia_tutores
            print("\nEstados en asistencia_tutores:")
            estados_tutores = conn.execute(text("""
                SELECT DISTINCT estado, COUNT(*) as cantidad
                FROM asistencia_tutores
                GROUP BY estado
                ORDER BY estado
            """)).fetchall()
            
            for estado in estados_tutores:
                print(f"  '{estado[0]}': {estado[1]} registros")
            
            # Verificar el tipo de columna estado
            print("\nTipo de columna estado en asistencia_estudiantes:")
            tipo_columna = conn.execute(text("""
                SELECT data_type, udt_name
                FROM information_schema.columns
                WHERE table_name = 'asistencia_estudiantes' AND column_name = 'estado'
            """)).fetchone()
            
            print(f"  Tipo: {tipo_columna[0]}, UDT: {tipo_columna[1]}")
            
            # Verificar valores del enum si existe
            print("\nValores del enum EstadoAsistencia:")
            try:
                enum_values = conn.execute(text("""
                    SELECT unnest(enum_range(NULL::estadoasistencia))
                """)).fetchall()
                
                for valor in enum_values:
                    print(f"  '{valor[0]}'")
            except Exception as e:
                print(f"  Error obteniendo valores del enum: {e}")
            
            # Calcular porcentajes con los valores correctos
            print("\nCalculando porcentajes con valores reales...")
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
            
            print("Muestra de porcentajes de asistencia:")
            for p in porcentajes:
                print(f"  {p[0]} {p[1]}: {p[3]}/{p[2]} = {p[4]}%")
            
            return True
            
    except Exception as e:
        print(f"Error verificando estados: {e}")
        return False

def main():
    """Función principal"""
    print("VERIFICANDO ESTADOS DE ASISTENCIA")
    print("=" * 50)
    
    success = check_attendance_states()
    
    if success:
        print("\nVerificacion completada!")
    else:
        print("\nError en la verificacion")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
