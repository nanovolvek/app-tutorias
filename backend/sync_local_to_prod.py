#!/usr/bin/env python3
"""
Script para sincronizar datos de la base de datos local a producción
IMPORTANTE: Este script debe ejecutarse solo una vez en producción
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

def get_local_connection():
    """Obtener conexión a la base de datos local"""
    local_db_url = os.getenv('LOCAL_DATABASE_URL', 'postgresql://postgres:nanopostgres@localhost:5432/tutorias_db')
    return create_engine(local_db_url)

def get_prod_connection():
    """Obtener conexión a la base de datos de producción"""
    prod_db_url = os.getenv('DATABASE_URL')
    if not prod_db_url:
        raise Exception("DATABASE_URL no está configurada")
    return create_engine(prod_db_url)

def sync_attendance_data():
    """Sincronizar datos de asistencia"""
    print("🔄 Sincronizando datos de asistencia...")
    
    local_engine = get_local_connection()
    prod_engine = get_prod_connection()
    
    # Obtener datos de asistencia de estudiantes de local
    with local_engine.connect() as local_conn:
        local_data = local_conn.execute(text("""
            SELECT estudiante_id, semana, estado, created_at, updated_at
            FROM asistencia_estudiantes
            ORDER BY estudiante_id, semana
        """)).fetchall()
    
    # Insertar en producción
    with prod_engine.connect() as prod_conn:
        # Limpiar datos existentes
        prod_conn.execute(text("DELETE FROM asistencia_estudiantes"))
        prod_conn.execute(text("DELETE FROM asistencia_tutores"))
        prod_conn.commit()
        
        # Insertar datos de estudiantes
        for row in local_data:
            prod_conn.execute(text("""
                INSERT INTO asistencia_estudiantes (estudiante_id, semana, estado, created_at, updated_at)
                VALUES (:estudiante_id, :semana, :estado, :created_at, :updated_at)
            """), {
                'estudiante_id': row[0],
                'semana': row[1],
                'estado': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            })
        
        # Obtener datos de asistencia de tutores de local
        local_tutor_data = local_conn.execute(text("""
            SELECT tutor_id, semana, estado, created_at, updated_at
            FROM asistencia_tutores
            ORDER BY tutor_id, semana
        """)).fetchall()
        
        # Insertar datos de tutores
        for row in local_tutor_data:
            prod_conn.execute(text("""
                INSERT INTO asistencia_tutores (tutor_id, semana, estado, created_at, updated_at)
                VALUES (:tutor_id, :semana, :estado, :created_at, :updated_at)
            """), {
                'tutor_id': row[0],
                'semana': row[1],
                'estado': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            })
        
        prod_conn.commit()
        print(f"✅ Sincronizados {len(local_data)} registros de asistencia de estudiantes")
        print(f"✅ Sincronizados {len(local_tutor_data)} registros de asistencia de tutores")

def sync_students_data():
    """Sincronizar datos de estudiantes actualizados"""
    print("🔄 Sincronizando datos de estudiantes...")
    
    local_engine = get_local_connection()
    prod_engine = get_prod_connection()
    
    # Obtener datos de estudiantes de local
    with local_engine.connect() as local_conn:
        students_data = local_conn.execute(text("""
            SELECT id, rut, nombre, apellido, curso, equipo_id, nombre_apoderado, 
                   contacto_apoderado, observaciones, created_at, updated_at
            FROM estudiantes
            ORDER BY id
        """)).fetchall()
    
    # Actualizar/insertar en producción
    with prod_engine.connect() as prod_conn:
        for student in students_data:
            prod_conn.execute(text("""
                INSERT INTO estudiantes (id, rut, nombre, apellido, curso, equipo_id, 
                                      nombre_apoderado, contacto_apoderado, observaciones, 
                                      created_at, updated_at)
                VALUES (:id, :rut, :nombre, :apellido, :curso, :equipo_id, 
                        :nombre_apoderado, :contacto_apoderado, :observaciones, 
                        :created_at, :updated_at)
                ON CONFLICT (id) DO UPDATE SET
                    rut = EXCLUDED.rut,
                    nombre = EXCLUDED.nombre,
                    apellido = EXCLUDED.apellido,
                    curso = EXCLUDED.curso,
                    equipo_id = EXCLUDED.equipo_id,
                    nombre_apoderado = EXCLUDED.nombre_apoderado,
                    contacto_apoderado = EXCLUDED.contacto_apoderado,
                    observaciones = EXCLUDED.observaciones,
                    updated_at = EXCLUDED.updated_at
            """), {
                'id': student[0],
                'rut': student[1],
                'nombre': student[2],
                'apellido': student[3],
                'curso': student[4],
                'equipo_id': student[5],
                'nombre_apoderado': student[6],
                'contacto_apoderado': student[7],
                'observaciones': student[8],
                'created_at': student[9],
                'updated_at': student[10]
            })
        
        prod_conn.commit()
        print(f"✅ Sincronizados {len(students_data)} estudiantes")

def sync_tutors_data():
    """Sincronizar datos de tutores actualizados"""
    print("🔄 Sincronizando datos de tutores...")
    
    local_engine = get_local_connection()
    prod_engine = get_prod_connection()
    
    # Obtener datos de tutores de local
    with local_engine.connect() as local_conn:
        tutors_data = local_conn.execute(text("""
            SELECT id, nombre, apellido, email, equipo_id, created_at, updated_at
            FROM tutores
            ORDER BY id
        """)).fetchall()
    
    # Actualizar/insertar en producción
    with prod_engine.connect() as prod_conn:
        for tutor in tutors_data:
            prod_conn.execute(text("""
                INSERT INTO tutores (id, nombre, apellido, email, equipo_id, created_at, updated_at)
                VALUES (:id, :nombre, :apellido, :email, :equipo_id, :created_at, :updated_at)
                ON CONFLICT (id) DO UPDATE SET
                    nombre = EXCLUDED.nombre,
                    apellido = EXCLUDED.apellido,
                    email = EXCLUDED.email,
                    equipo_id = EXCLUDED.equipo_id,
                    updated_at = EXCLUDED.updated_at
            """), {
                'id': tutor[0],
                'nombre': tutor[1],
                'apellido': tutor[2],
                'email': tutor[3],
                'equipo_id': tutor[4],
                'created_at': tutor[5],
                'updated_at': tutor[6]
            })
        
        prod_conn.commit()
        print(f"✅ Sincronizados {len(tutors_data)} tutores")

def update_sequences():
    """Actualizar secuencias de ID en producción"""
    print("🔄 Actualizando secuencias de ID...")
    
    prod_engine = get_prod_connection()
    
    with prod_engine.connect() as prod_conn:
        # Actualizar secuencia de estudiantes
        max_student_id = prod_conn.execute(text("SELECT COALESCE(MAX(id), 0) FROM estudiantes")).scalar()
        prod_conn.execute(text(f"ALTER SEQUENCE estudiantes_id_seq RESTART WITH {max_student_id + 1}"))
        
        # Actualizar secuencia de tutores
        max_tutor_id = prod_conn.execute(text("SELECT COALESCE(MAX(id), 0) FROM tutores")).scalar()
        prod_conn.execute(text(f"ALTER SEQUENCE tutores_id_seq RESTART WITH {max_tutor_id + 1}"))
        
        # Actualizar secuencia de asistencia_estudiantes
        max_attendance_id = prod_conn.execute(text("SELECT COALESCE(MAX(id), 0) FROM asistencia_estudiantes")).scalar()
        prod_conn.execute(text(f"ALTER SEQUENCE asistencia_estudiantes_id_seq RESTART WITH {max_attendance_id + 1}"))
        
        # Actualizar secuencia de asistencia_tutores
        max_tutor_attendance_id = prod_conn.execute(text("SELECT COALESCE(MAX(id), 0) FROM asistencia_tutores")).scalar()
        prod_conn.execute(text(f"ALTER SEQUENCE asistencia_tutores_id_seq RESTART WITH {max_tutor_attendance_id + 1}"))
        
        prod_conn.commit()
        print("✅ Secuencias actualizadas correctamente")

def main():
    """Función principal de sincronización"""
    print("🚀 Iniciando sincronización de datos local → producción")
    print("⚠️  ADVERTENCIA: Este script modificará la base de datos de producción")
    
    try:
        # Verificar que estamos en producción
        if not os.getenv('DATABASE_URL') or 'localhost' in os.getenv('DATABASE_URL', ''):
            print("❌ Error: No se detectó configuración de producción")
            print("   Asegúrate de que DATABASE_URL apunte a la base de datos de producción")
            return False
        
        # Ejecutar sincronización
        sync_students_data()
        sync_tutors_data()
        sync_attendance_data()
        update_sequences()
        
        print("🎉 Sincronización completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
