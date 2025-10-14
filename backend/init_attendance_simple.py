#!/usr/bin/env python3
"""
Script simple para inicializar datos de asistencia usando valores directos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.database import DATABASE_URL

def init_attendance_simple():
    """Inicializar datos de asistencia usando SQL directo"""
    
    print("Inicializando datos de asistencia...")
    
    # Crear engine
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Obtener estudiantes
            result = conn.execute(text("SELECT id FROM students;"))
            student_ids = [row[0] for row in result]
            print(f"Encontrados {len(student_ids)} estudiantes")
            
            # Obtener tutores
            result = conn.execute(text("SELECT id FROM tutors;"))
            tutor_ids = [row[0] for row in result]
            print(f"Encontrados {len(tutor_ids)} tutores")
            
            # Inicializar asistencia para estudiantes
            student_count = 0
            for student_id in student_ids:
                for week_num in range(1, 11):
                    week_key = f"semana_{week_num}"
                    
                    # Verificar si ya existe
                    result = conn.execute(text("""
                        SELECT id FROM student_attendance 
                        WHERE student_id = :student_id AND week = :week
                    """), {"student_id": student_id, "week": week_key})
                    
                    if not result.fetchone():
                        # Crear registro con estado aleatorio
                        import random
                        statuses = ["asistió", "no asistió", "tutoría suspendida", "vacaciones/feriado"]
                        # 70% de probabilidad de asistir
                        status = "asistió" if random.random() < 0.7 else random.choice(statuses)
                        
                        conn.execute(text("""
                            INSERT INTO student_attendance (student_id, week, status)
                            VALUES (:student_id, :week, :status)
                        """), {
                            "student_id": student_id,
                            "week": week_key,
                            "status": status
                        })
                        student_count += 1
            
            # Inicializar asistencia para tutores
            tutor_count = 0
            for tutor_id in tutor_ids:
                for week_num in range(1, 11):
                    week_key = f"semana_{week_num}"
                    
                    # Verificar si ya existe
                    result = conn.execute(text("""
                        SELECT id FROM tutor_attendance 
                        WHERE tutor_id = :tutor_id AND week = :week
                    """), {"tutor_id": tutor_id, "week": week_key})
                    
                    if not result.fetchone():
                        # Crear registro con estado aleatorio
                        import random
                        statuses = ["asistió", "no asistió", "tutoría suspendida", "vacaciones/feriado"]
                        # 80% de probabilidad de asistir (tutores más responsables)
                        status = "asistió" if random.random() < 0.8 else random.choice(statuses)
                        
                        conn.execute(text("""
                            INSERT INTO tutor_attendance (tutor_id, week, status)
                            VALUES (:tutor_id, :week, :status)
                        """), {
                            "tutor_id": tutor_id,
                            "week": week_key,
                            "status": status
                        })
                        tutor_count += 1
            
            conn.commit()
            
            print(f"Se crearon {student_count} registros de asistencia para estudiantes")
            print(f"Se crearon {tutor_count} registros de asistencia para tutores")
            print("Datos de asistencia inicializados exitosamente!")
            
    except Exception as e:
        print(f"Error al inicializar datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = init_attendance_simple()
    sys.exit(0 if success else 1)
