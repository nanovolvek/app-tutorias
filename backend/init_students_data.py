#!/usr/bin/env python3
"""
Script para inicializar datos de estudiantes con RUTs y apoderados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Student, School, Attendance
import random

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

def generate_rut():
    """Generar un RUT chileno válido"""
    # Generar número aleatorio entre 10.000.000 y 25.000.000
    number = random.randint(10000000, 25000000)
    
    # Calcular dígito verificador
    def calculate_dv(number):
        reversed_digits = list(map(int, reversed(str(number))))
        factors = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7]
        sum_ = sum(digit * factor for digit, factor in zip(reversed_digits, factors))
        remainder = sum_ % 11
        dv = 11 - remainder
        if dv == 11:
            return '0'
        elif dv == 10:
            return 'K'
        else:
            return str(dv)
    
    dv = calculate_dv(number)
    return f"{number:,}".replace(',', '.') + f"-{dv}"

def init_students_data():
    """Inicializar datos de estudiantes con RUTs y apoderados"""
    db = SessionLocal()
    
    try:
        # Verificar que existen colegios
        schools = db.query(School).all()
        if not schools:
            print("No hay colegios en la base de datos. Primero ejecuta init_db.py")
            return
        
        # Datos de estudiantes de ejemplo
        students_data = [
            {
                "first_name": "Ana",
                "last_name": "Silva",
                "course": "3° Básico",
                "school_id": 1,
                "guardian_name": "María Silva",
                "guardian_contact": "+56 9 1234 5678",
                "observations": "Estudiante muy participativa, necesita apoyo en matemáticas"
            },
            {
                "first_name": "Diego",
                "last_name": "Martínez",
                "course": "1° Medio",
                "school_id": 2,
                "guardian_name": "Carlos Martínez",
                "guardian_contact": "carlos.martinez@email.com",
                "observations": "Excelente rendimiento, líder natural del grupo"
            },
            {
                "first_name": "Sofía",
                "last_name": "López",
                "course": "5° Básico",
                "school_id": 1,
                "guardian_name": "Patricia López",
                "guardian_contact": "+56 9 8765 4321",
                "observations": "Necesita mejorar en lectura comprensiva"
            },
            {
                "first_name": "Sebastián",
                "last_name": "González",
                "course": "2° Medio",
                "school_id": 2,
                "guardian_name": "Roberto González",
                "guardian_contact": "roberto.gonzalez@email.com",
                "observations": "Interesado en ciencias, muy creativo"
            },
            {
                "first_name": "Valentina",
                "last_name": "Rodríguez",
                "course": "4° Básico",
                "school_id": 1,
                "guardian_name": "Carmen Rodríguez",
                "guardian_contact": "+56 9 5555 1234",
                "observations": "Buena asistencia, participa activamente"
            },
            {
                "first_name": "Matías",
                "last_name": "Herrera",
                "course": "3° Medio",
                "school_id": 2,
                "guardian_name": "Luis Herrera",
                "guardian_contact": "luis.herrera@email.com",
                "observations": "Necesita apoyo en inglés, muy motivado"
            },
            {
                "first_name": "Isabella",
                "last_name": "Vargas",
                "course": "6° Básico",
                "school_id": 1,
                "guardian_name": "Elena Vargas",
                "guardian_contact": "+56 9 3333 7777",
                "observations": "Excelente en artes, necesita apoyo en ciencias"
            },
            {
                "first_name": "Nicolás",
                "last_name": "Torres",
                "course": "1° Básico",
                "school_id": 1,
                "guardian_name": "Andrea Torres",
                "guardian_contact": "andrea.torres@email.com",
                "observations": "Primer año, muy entusiasta y colaborador"
            }
        ]
        
        print("Creando estudiantes con RUTs y datos de apoderados...")
        
        for student_data in students_data:
            # Generar RUT único
            rut = generate_rut()
            
            # Verificar que el RUT no existe
            while db.query(Student).filter(Student.rut == rut).first():
                rut = generate_rut()
            
            student = Student(
                rut=rut,
                first_name=student_data["first_name"],
                last_name=student_data["last_name"],
                course=student_data["course"],
                school_id=student_data["school_id"],
                guardian_name=student_data["guardian_name"],
                guardian_contact=student_data["guardian_contact"],
                observations=student_data["observations"]
            )
            
            db.add(student)
            print(f"Creado: {student.first_name} {student.last_name} - RUT: {student.rut}")
        
        db.commit()
        print(f"\nSe crearon {len(students_data)} estudiantes exitosamente")
        
        # Inicializar datos de asistencia para todos los estudiantes
        print("\nInicializando datos de asistencia...")
        all_students = db.query(Student).all()
        
        for student in all_students:
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
        print("\n=== RESUMEN DE ESTUDIANTES ===")
        for student in all_students:
            attendance_records = db.query(Attendance).filter(
                Attendance.student_id == student.id
            ).all()
            
            attended_count = sum(1 for record in attendance_records if record.attended)
            percentage = (attended_count / 10) * 100
            
            print(f"{student.first_name} {student.last_name} ({student.rut})")
            print(f"  Curso: {student.course}")
            print(f"  Apoderado: {student.guardian_name}")
            print(f"  Contacto: {student.guardian_contact}")
            print(f"  Asistencia: {attended_count}/10 semanas ({percentage:.1f}%)")
            print(f"  Observaciones: {student.observations}")
            print()
    
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_students_data()
