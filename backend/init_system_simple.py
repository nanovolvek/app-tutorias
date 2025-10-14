#!/usr/bin/env python3
"""
Script simple para inicializar el sistema sin emojis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Student, School, Tutor, User, Attendance
from app.auth.security import get_password_hash
import random

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

def generate_rut():
    """Generar un RUT chileno válido"""
    number = random.randint(10000000, 25000000)
    
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

def init_system():
    """Inicializar el sistema con datos de prueba"""
    db = SessionLocal()
    
    try:
        print("=== INICIALIZANDO SISTEMA ===")
        
        # 1. Crear colegios
        print("1. Creando colegios...")
        schools_data = [
            {"name": "Colegio San Patricio", "comuna": "Las Condes"},
            {"name": "Liceo Manuel Barros Borgoño", "comuna": "Santiago"},
            {"name": "Instituto Nacional", "comuna": "Santiago"},
            {"name": "Colegio San Ignacio", "comuna": "Providencia"}
        ]
        
        for school_data in schools_data:
            existing = db.query(School).filter(School.name == school_data["name"]).first()
            if not existing:
                school = School(**school_data)
                db.add(school)
                print(f"  - {school_data['name']} - {school_data['comuna']}")
        
        db.commit()
        
        # 2. Crear usuarios
        print("\n2. Creando usuarios...")
        users_data = [
            {
                "email": "admin@tutorias.com",
                "full_name": "Administrador Sistema",
                "role": "admin",
                "hashed_password": get_password_hash("admin123")
            },
            {
                "email": "tutor1@tutorias.com",
                "full_name": "Maria Gonzalez",
                "role": "tutor",
                "hashed_password": get_password_hash("tutor123")
            }
        ]
        
        for user_data in users_data:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(**user_data)
                db.add(user)
                print(f"  - {user_data['email']} - {user_data['role']}")
        
        db.commit()
        
        # 3. Crear tutores
        print("\n3. Creando tutores...")
        tutors_data = [
            {
                "first_name": "Maria",
                "last_name": "Gonzalez",
                "email": "maria.gonzalez@tutorias.com",
                "school_id": 1
            },
            {
                "first_name": "Carlos",
                "last_name": "Perez",
                "email": "carlos.perez@tutorias.com",
                "school_id": 2
            }
        ]
        
        for tutor_data in tutors_data:
            existing = db.query(Tutor).filter(Tutor.email == tutor_data["email"]).first()
            if not existing:
                tutor = Tutor(**tutor_data)
                db.add(tutor)
                print(f"  - {tutor_data['first_name']} {tutor_data['last_name']}")
        
        db.commit()
        
        # 4. Crear estudiantes
        print("\n4. Creando estudiantes...")
        students_data = [
            {
                "first_name": "Ana",
                "last_name": "Silva",
                "course": "3° Básico",
                "school_id": 1,
                "guardian_name": "Maria Silva",
                "guardian_contact": "+56 9 1234 5678",
                "observations": "Estudiante muy participativa, necesita apoyo en matematicas"
            },
            {
                "first_name": "Diego",
                "last_name": "Martinez",
                "course": "1° Medio",
                "school_id": 2,
                "guardian_name": "Carlos Martinez",
                "guardian_contact": "carlos.martinez@email.com",
                "observations": "Excelente rendimiento, lider natural del grupo"
            },
            {
                "first_name": "Sofia",
                "last_name": "Lopez",
                "course": "5° Básico",
                "school_id": 1,
                "guardian_name": "Patricia Lopez",
                "guardian_contact": "+56 9 8765 4321",
                "observations": "Necesita mejorar en lectura comprensiva"
            },
            {
                "first_name": "Sebastian",
                "last_name": "Gonzalez",
                "course": "2° Medio",
                "school_id": 2,
                "guardian_name": "Roberto Gonzalez",
                "guardian_contact": "roberto.gonzalez@email.com",
                "observations": "Interesado en ciencias, muy creativo"
            },
            {
                "first_name": "Valentina",
                "last_name": "Rodriguez",
                "course": "4° Básico",
                "school_id": 1,
                "guardian_name": "Carmen Rodriguez",
                "guardian_contact": "+56 9 5555 1234",
                "observations": "Buena asistencia, participa activamente"
            }
        ]
        
        for student_data in students_data:
            # Generar RUT único
            rut = generate_rut()
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
            print(f"  - {student.first_name} {student.last_name} - RUT: {student.rut}")
        
        db.commit()
        
        # 5. Crear datos de asistencia
        print("\n5. Creando datos de asistencia...")
        all_students = db.query(Student).all()
        
        for student in all_students:
            for week_num in range(1, 11):
                week_key = f"semana_{week_num}"
                
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
        print(f"  - Datos de asistencia creados para {len(all_students)} estudiantes")
        
        # 6. Mostrar resumen
        print("\n=== RESUMEN DEL SISTEMA ===")
        schools_count = db.query(School).count()
        users_count = db.query(User).count()
        tutors_count = db.query(Tutor).count()
        students_count = db.query(Student).count()
        attendance_count = db.query(Attendance).count()
        
        print(f"Colegios: {schools_count}")
        print(f"Usuarios: {users_count}")
        print(f"Tutores: {tutors_count}")
        print(f"Estudiantes: {students_count}")
        print(f"Registros de asistencia: {attendance_count}")
        
        print("\n=== CREDENCIALES DE ACCESO ===")
        print("Admin: admin@tutorias.com / admin123")
        print("Tutor: tutor1@tutorias.com / tutor123")
        
        print("\n=== ESTUDIANTES CREADOS ===")
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
            print()
        
        print("Sistema inicializado correctamente!")
        print("\nPara probar el sistema:")
        print("1. Ejecuta: uvicorn app.main:app --reload --port 8000")
        print("2. En otra terminal: npm run dev")
        print("3. Ve a http://localhost:5173 y haz login")
    
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_system()
