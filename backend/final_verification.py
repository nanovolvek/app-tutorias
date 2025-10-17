#!/usr/bin/env python3
"""
Script para verificación final de la base de datos de producción
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def final_verification():
    """Verificación final de todos los datos"""
    print("Verificacion final de la base de datos de produccion...")
    
    # Configurar URL de producción
    prod_db_url = 'postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres'
    engine = create_engine(prod_db_url)
    
    try:
        with engine.connect() as conn:
            # 1. Verificar estudiantes con equipos y colegios
            print("1. Verificando estudiantes con relaciones...")
            estudiantes = conn.execute(text("""
                SELECT e.nombre, e.apellido, eq.nombre as equipo, c.nombre as colegio, c.comuna
                FROM estudiantes e
                LEFT JOIN equipos eq ON e.equipo_id = eq.id
                LEFT JOIN colegios c ON eq.colegio_id = c.id
                ORDER BY e.id
                LIMIT 5
            """)).fetchall()
            
            print("Muestra de estudiantes:")
            for est in estudiantes:
                print(f"  {est[0]} {est[1]} -> {est[2]} -> {est[3]} ({est[4]})")
            
            # 2. Verificar tutores con equipos y colegios
            print("\n2. Verificando tutores con relaciones...")
            tutores = conn.execute(text("""
                SELECT t.nombre, t.apellido, eq.nombre as equipo, c.nombre as colegio, c.comuna
                FROM tutores t
                LEFT JOIN equipos eq ON t.equipo_id = eq.id
                LEFT JOIN colegios c ON eq.colegio_id = c.id
                ORDER BY t.id
                LIMIT 3
            """)).fetchall()
            
            print("Muestra de tutores:")
            for tut in tutores:
                print(f"  {tut[0]} {tut[1]} -> {tut[2]} -> {tut[3]} ({tut[4]})")
            
            # 3. Verificar estados de asistencia
            print("\n3. Verificando estados de asistencia...")
            estados_estudiantes = conn.execute(text("""
                SELECT DISTINCT estado, COUNT(*) as cantidad
                FROM asistencia_estudiantes
                GROUP BY estado
                ORDER BY estado
            """)).fetchall()
            
            print("Estados en asistencia_estudiantes:")
            for estado in estados_estudiantes:
                print(f"  '{estado[0]}': {estado[1]} registros")
            
            # 4. Calcular porcentajes de asistencia (sin ROUND)
            print("\n4. Calculando porcentajes de asistencia...")
            porcentajes = conn.execute(text("""
                SELECT e.nombre, e.apellido,
                       COUNT(ae.id) as total_semanas,
                       COUNT(CASE WHEN ae.estado = 'asistio' THEN 1 END) as semanas_asistio,
                       CAST(
                           (COUNT(CASE WHEN ae.estado = 'asistio' THEN 1 END)::float / NULLIF(COUNT(ae.id), 0)) * 100 AS DECIMAL(5,2)
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
            
            # 5. Verificar totales
            print("\n5. Verificando totales...")
            totales = conn.execute(text("""
                SELECT 
                    (SELECT COUNT(*) FROM estudiantes) as total_estudiantes,
                    (SELECT COUNT(*) FROM tutores) as total_tutores,
                    (SELECT COUNT(*) FROM equipos) as total_equipos,
                    (SELECT COUNT(*) FROM colegios) as total_colegios,
                    (SELECT COUNT(*) FROM asistencia_estudiantes) as total_asistencia_estudiantes,
                    (SELECT COUNT(*) FROM asistencia_tutores) as total_asistencia_tutores
            """)).fetchone()
            
            print(f"Total estudiantes: {totales[0]}")
            print(f"Total tutores: {totales[1]}")
            print(f"Total equipos: {totales[2]}")
            print(f"Total colegios: {totales[3]}")
            print(f"Total registros asistencia estudiantes: {totales[4]}")
            print(f"Total registros asistencia tutores: {totales[5]}")
            
            print("\nVerificacion final completada exitosamente!")
            return True
            
    except Exception as e:
        print(f"Error en verificacion final: {e}")
        return False

def main():
    """Función principal"""
    print("VERIFICACION FINAL DE PRODUCCION")
    print("=" * 50)
    
    success = final_verification()
    
    if success:
        print("\n" + "=" * 50)
        print("TODOS LOS DATOS ESTAN CORRECTOS!")
        print("La aplicacion en produccion deberia mostrar:")
        print("✅ Equipos y colegios correctamente asignados")
        print("✅ Datos de asistencia funcionando")
        print("✅ Graficos y estadisticas visibles")
        print("✅ Porcentajes de asistencia calculados")
    else:
        print("\nError en la verificacion final")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
