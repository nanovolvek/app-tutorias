#!/usr/bin/env python3
"""
Script para inicializar datos de asistencia en las nuevas tablas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models.attendance import StudentAttendance, TutorAttendance, AttendanceStatus
from app.models.student import Student
from app.models.tutor import Tutor

def init_attendance_data():
    """Inicializar datos de asistencia para estudiantes y tutores"""
    
    print("Inicializando datos de asistencia...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Obtener todos los estudiantes
        students = db.query(Student).all()
        print(f"Encontrados {len(students)} estudiantes")
        
        # Obtener todos los tutores
        tutors = db.query(Tutor).all()
        print(f"Encontrados {len(tutors)} tutores")
        
        # Inicializar asistencia para estudiantes
        student_count = 0
        for student in students:
            for week_num in range(1, 11):
                week_key = f"semana_{week_num}"
                
                # Verificar si ya existe un registro
                existing = db.query(StudentAttendance).filter(
                    StudentAttendance.student_id == student.id,
                    StudentAttendance.week == week_key
                ).first()
                
                if not existing:
                    # Crear registro con estado aleatorio para demostración
                    import random
                    statuses = [
                        AttendanceStatus.ATTENDED,
                        AttendanceStatus.NOT_ATTENDED,
                        AttendanceStatus.SUSPENDED,
                        AttendanceStatus.VACATION
                    ]
                    # 70% de probabilidad de asistir
                    status = AttendanceStatus.ATTENDED if random.random() < 0.7 else random.choice(statuses)
                    
                    attendance_record = StudentAttendance(
                        student_id=student.id,
                        week=week_key,
                        status=status
                    )
                    db.add(attendance_record)
                    student_count += 1
        
        # Inicializar asistencia para tutores
        tutor_count = 0
        for tutor in tutors:
            for week_num in range(1, 11):
                week_key = f"semana_{week_num}"
                
                # Verificar si ya existe un registro
                existing = db.query(TutorAttendance).filter(
                    TutorAttendance.tutor_id == tutor.id,
                    TutorAttendance.week == week_key
                ).first()
                
                if not existing:
                    # Crear registro con estado aleatorio para demostración
                    import random
                    statuses = [
                        AttendanceStatus.ATTENDED,
                        AttendanceStatus.NOT_ATTENDED,
                        AttendanceStatus.SUSPENDED,
                        AttendanceStatus.VACATION
                    ]
                    # 80% de probabilidad de asistir (tutores más responsables)
                    status = AttendanceStatus.ATTENDED if random.random() < 0.8 else random.choice(statuses)
                    
                    attendance_record = TutorAttendance(
                        tutor_id=tutor.id,
                        week=week_key,
                        status=status
                    )
                    db.add(attendance_record)
                    tutor_count += 1
        
        # Guardar cambios
        db.commit()
        
        print(f"Se crearon {student_count} registros de asistencia para estudiantes")
        print(f"Se crearon {tutor_count} registros de asistencia para tutores")
        print("Datos de asistencia inicializados exitosamente!")
        
    except Exception as e:
        print(f"Error al inicializar datos: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    success = init_attendance_data()
    sys.exit(0 if success else 1)
