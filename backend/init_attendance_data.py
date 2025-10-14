#!/usr/bin/env python3
"""
Script para inicializar datos de asistencia de prueba
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Student, Attendance
import random

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

def init_attendance_data():
    """Inicializar datos de asistencia de prueba"""
    db = SessionLocal()
    
    try:
        # Obtener todos los estudiantes
        students = db.query(Student).all()
        
        if not students:
            print("No hay estudiantes en la base de datos. Primero ejecuta init_db.py")
            return
        
        print(f"Encontrados {len(students)} estudiantes")
        
        # Para cada estudiante, crear registros de asistencia para 10 semanas
        for student in students:
            print(f"Inicializando asistencia para {student.first_name} {student.last_name}")
            
            for week_num in range(1, 11):
                week_key = f"semana_{week_num}"
                
                # Verificar si ya existe un registro para esta semana
                existing = db.query(Attendance).filter(
                    Attendance.student_id == student.id,
                    Attendance.week == week_key
                ).first()
                
                if not existing:
                    # Generar asistencia aleatoria (70% de probabilidad de asistir)
                    attended = random.random() < 0.7
                    
                    attendance_record = Attendance(
                        student_id=student.id,
                        week=week_key,
                        attended=attended
                    )
                    db.add(attendance_record)
        
        db.commit()
        print("Datos de asistencia inicializados correctamente")
        
        # Mostrar resumen
        for student in students:
            attendance_records = db.query(Attendance).filter(
                Attendance.student_id == student.id
            ).all()
            
            attended_count = sum(1 for record in attendance_records if record.attended)
            percentage = (attended_count / 10) * 100
            
            print(f"{student.first_name} {student.last_name}: {attended_count}/10 semanas ({percentage:.1f}%)")
    
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_attendance_data()
