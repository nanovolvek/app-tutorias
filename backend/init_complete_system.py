#!/usr/bin/env python3
"""
Script completo para inicializar todo el sistema con datos de prueba
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

def init_complete_system():
    """Inicializar todo el sistema con datos de prueba"""
    db = SessionLocal()
    
    try:
        print("=== INICIALIZANDO SISTEMA COMPLETO ===\n")
        
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
                print(f"  ✓ {school_data['name']} - {school_data['comuna']}")
        
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
                "full_name": "María González",
                "role": "tutor",
                "hashed_password": get_password_hash("tutor123")
            },
            {
                "email": "tutor2@tutorias.com",
                "full_name": "Carlos Pérez",
                "role": "tutor",
                "hashed_password": get_password_hash("tutor123")
            }
        ]
        
        for user_data in users_data:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(**user_data)
                db.add(user)
                print(f"  ✓ {user_data['email']} - {user_data['role']}")
        
        db.commit()
        
        # 3. Crear tutores
        print("\n3. Creando tutores...")
        tutors_data = [
            {
                "first_name": "María",
                "last_name": "González",
                "email": "maria.gonzalez@tutorias.com",
                "school_id": 1
            },
            {
                "first_name": "Carlos",
                "last_name": "Pérez",
                "email": "carlos.perez@tutorias.com",
                "school_id": 2
            },
            {
                "first_name": "Ana",
                "last_name": "Rodríguez",
                "email": "ana.rodriguez@tutorias.com",
                "school_id": 1
            }
        ]
        
        for tutor_data in tutors_data:
            existing = db.query(Tutor).filter(Tutor.email == tutor_data["email"]).first()
            if not existing:
                tutor = Tutor(**tutor_data)
                db.add(tutor)
                print(f"  ✓ {tutor_data['first_name']} {tutor_data['last_name']}")
        
        db.commit()
        
        # 4. Crear estudiantes
        print("\n4. Creando estudiantes...")
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
            },
            {
                "first_name": "Camila",
                "last_name": "Morales",
                "course": "2° Básico",
                "school_id": 2,
                "guardian_name": "Pedro Morales",
                "guardian_contact": "+56 9 4444 8888",
                "observations": "Muy tímida, necesita confianza para participar"
            },
            {
                "first_name": "Joaquín",
                "last_name": "Castro",
                "course": "4° Medio",
                "school_id": 2,
                "guardian_name": "Rosa Castro",
                "guardian_contact": "rosa.castro@email.com",
                "observations": "Preparándose para PSU, muy dedicado"
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
            print(f"  ✓ {student.first_name} {student.last_name} - RUT: {student.rut}")
        
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
        print(f"  ✓ Datos de asistencia creados para {len(all_students)} estudiantes")
        
        # 6. Mostrar resumen final
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
        print("Tutor 1: tutor1@tutorias.com / tutor123")
        print("Tutor 2: tutor2@tutorias.com / tutor123")
        
        print("\n=== ESTUDIANTES CREADOS ===")
        for student in all_students:
            attendance_records = db.query(Attendance).filter(
                Attendance.student_id == student.id
            ).all()
            
            attended_count = sum(1 for record in attendance_records if record.attended)
            percentage = (attended_count / 10) * 100
            
            print(f"{student.first_name} {student.last_name} ({student.rut})")
            print(f"  Curso: {student.course} | Asistencia: {attended_count}/10 ({percentage:.1f}%)")
            print(f"  Apoderado: {student.guardian_name} | Contacto: {student.guardian_contact}")
            print()
        
        print("✅ Sistema inicializado correctamente!")
        print("\nPara probar el sistema:")
        print("1. Ejecuta: uvicorn app.main:app --reload --port 8000")
        print("2. En otra terminal: npm run dev")
        print("3. Ve a http://localhost:5173 y haz login")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_complete_system()
