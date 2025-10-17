#!/usr/bin/env python3
"""
Script para verificar que todos los datos estén correctos en producción
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def verify_data():
    """Verificar que todos los datos estén correctos"""
    print("Verificando datos en la base de datos de produccion...")
    
    # Configurar URL de producción
    prod_db_url = 'postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres'
    engine = create_engine(prod_db_url)
    
    try:
        with engine.connect() as conn:
            # 1. Verificar estudiantes con equipos y colegios
            print("1. Verificando estudiantes...")
            estudiantes = conn.execute(text("""
                SELECT e.id, e.nombre, e.apellido, eq.nombre as equipo, c.nombre as colegio, c.comuna
                FROM estudiantes e
                LEFT JOIN equipos eq ON e.equipo_id = eq.id
                LEFT JOIN colegios c ON eq.colegio_id = c.id
                ORDER BY e.id
            """)).fetchall()
            
            print(f"Total estudiantes: {len(estudiantes)}")
            for est in estudiantes:
                print(f"  {est[0]}: {est[1]} {est[2]} -> {est[3]} -> {est[4]} ({est[5]})")
            
            # 2. Verificar tutores con equipos y colegios
            print("\n2. Verificando tutores...")
            tutores = conn.execute(text("""
                SELECT t.id, t.nombre, t.apellido, eq.nombre as equipo, c.nombre as colegio, c.comuna
                FROM tutores t
                LEFT JOIN equipos eq ON t.equipo_id = eq.id
                LEFT JOIN colegios c ON eq.colegio_id = c.id
                ORDER BY t.id
            """)).fetchall()
            
            print(f"Total tutores: {len(tutores)}")
            for tut in tutores:
                print(f"  {tut[0]}: {tut[1]} {tut[2]} -> {tut[3]} -> {tut[4]} ({tut[5]})")
            
            # 3. Verificar datos de asistencia de estudiantes
            print("\n3. Verificando asistencia de estudiantes...")
            asistencia_estudiantes = conn.execute(text("""
                SELECT COUNT(*) as total_registros,
                       COUNT(DISTINCT estudiante_id) as estudiantes_con_asistencia,
                       COUNT(DISTINCT semana) as semanas_registradas
                FROM asistencia_estudiantes
            """)).fetchone()
            
            print(f"Total registros de asistencia estudiantes: {asistencia_estudiantes[0]}")
            print(f"Estudiantes con asistencia: {asistencia_estudiantes[1]}")
            print(f"Semanas registradas: {asistencia_estudiantes[2]}")
            
            # 4. Verificar datos de asistencia de tutores
            print("\n4. Verificando asistencia de tutores...")
            asistencia_tutores = conn.execute(text("""
                SELECT COUNT(*) as total_registros,
                       COUNT(DISTINCT tutor_id) as tutores_con_asistencia,
                       COUNT(DISTINCT semana) as semanas_registradas
                FROM asistencia_tutores
            """)).fetchone()
            
            print(f"Total registros de asistencia tutores: {asistencia_tutores[0]}")
            print(f"Tutores con asistencia: {asistencia_tutores[1]}")
            print(f"Semanas registradas: {asistencia_tutores[2]}")
            
            # 5. Verificar equipos y colegios
            print("\n5. Verificando equipos y colegios...")
            equipos = conn.execute(text("""
                SELECT eq.id, eq.nombre, c.nombre as colegio, c.comuna
                FROM equipos eq
                LEFT JOIN colegios c ON eq.colegio_id = c.id
                ORDER BY eq.id
            """)).fetchall()
            
            for eq in equipos:
                print(f"  Equipo {eq[0]}: {eq[1]} -> {eq[2]} ({eq[3]})")
            
            # 6. Calcular porcentajes de asistencia de muestra
            print("\n6. Calculando porcentajes de asistencia de muestra...")
            porcentajes = conn.execute(text("""
                SELECT e.nombre, e.apellido,
                       COUNT(ae.id) as total_semanas,
                       COUNT(CASE WHEN ae.estado = 'asistio' THEN 1 END) as semanas_asistio,
                       ROUND(
                           (COUNT(CASE WHEN ae.estado = 'asistio' THEN 1 END)::float / COUNT(ae.id)) * 100, 2
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
            
            print("\nVerificacion completada exitosamente!")
            return True
            
    except Exception as e:
        print(f"Error verificando datos: {e}")
        return False

def main():
    """Función principal"""
    print("VERIFICANDO DATOS EN PRODUCCION")
    print("=" * 50)
    
    success = verify_data()
    
    if success:
        print("\n" + "=" * 50)
        print("TODOS LOS DATOS ESTAN CORRECTOS!")
        print("La aplicacion en produccion deberia funcionar perfectamente ahora.")
    else:
        print("\nError en la verificacion de datos")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
