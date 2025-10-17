#!/usr/bin/env python3
"""
Script corregido para inicializar el sistema con datos de prueba
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Student, School, Tutor, User, Attendance
from app.models.attendance import StudentAttendance, AttendanceStatus
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

def init_data_fixed():
    """Inicializar el sistema con datos de prueba usando los nombres correctos de campos"""
    db = SessionLocal()
    
    try:
        print("=== INICIALIZANDO SISTEMA CORREGIDO ===\n")
        
        # 1. Crear colegios
        print("1. Creando colegios...")
        schools_data = [
            {"nombre": "Colegio San Patricio", "comuna": "Las Condes"},
            {"nombre": "Liceo Manuel Barros Borgoño", "comuna": "Santiago"},
            {"nombre": "Instituto Nacional", "comuna": "Santiago"},
            {"nombre": "Colegio San Ignacio", "comuna": "Providencia"}
        ]
        
        for school_data in schools_data:
            existing = db.query(School).filter(School.nombre == school_data["nombre"]).first()
            if not existing:
                school = School(**school_data)
                db.add(school)
                print(f"  [OK] {school_data['nombre']} - {school_data['comuna']}")
        
        db.commit()
        
        # 2. Crear usuarios
        print("\n2. Creando usuarios...")
        users_data = [
            {
                "email": "admin@tutorias.com",
                "nombre_completo": "Administrador Sistema",
                "rol": "admin",
                "contrasena_hash": get_password_hash("admin123")
            },
            {
                "email": "tutor1@tutorias.com",
                "nombre_completo": "María González",
                "rol": "tutor",
                "contrasena_hash": get_password_hash("tutor123")
            },
            {
                "email": "tutor2@tutorias.com",
                "nombre_completo": "Carlos Pérez",
                "rol": "tutor",
                "contrasena_hash": get_password_hash("tutor123")
            }
        ]
        
        for user_data in users_data:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(**user_data)
                db.add(user)
                print(f"  [OK] {user_data['email']} - {user_data['rol']}")
        
        db.commit()
        
        # 3. Crear tutores
        print("\n3. Creando tutores...")
        # Obtener los IDs de los colegios creados
        colegios = db.query(School).all()
        colegio_ids = [c.id for c in colegios]
        
        tutors_data = [
            {
                "nombre": "María",
                "apellido": "González",
                "email": "maria.gonzalez@tutorias.com",
                "id_colegio": colegio_ids[0]
            },
            {
                "nombre": "Carlos",
                "apellido": "Pérez",
                "email": "carlos.perez@tutorias.com",
                "id_colegio": colegio_ids[1]
            },
            {
                "nombre": "Ana",
                "apellido": "Rodríguez",
                "email": "ana.rodriguez@tutorias.com",
                "id_colegio": colegio_ids[0]
            }
        ]
        
        for tutor_data in tutors_data:
            existing = db.query(Tutor).filter(Tutor.email == tutor_data["email"]).first()
            if not existing:
                tutor = Tutor(**tutor_data)
                db.add(tutor)
                print(f"  [OK] {tutor_data['nombre']} {tutor_data['apellido']}")
        
        db.commit()
        
        # 4. Crear estudiantes
        print("\n4. Creando estudiantes...")
        # Obtener los IDs de los colegios creados
        colegios = db.query(School).all()
        colegio_ids = [c.id for c in colegios]
        
        students_data = [
            {
                "nombre": "Ana",
                "apellido": "Silva",
                "curso": "3° Básico",
                "id_colegio": colegio_ids[0],
                "nombre_apoderado": "María Silva",
                "contacto_apoderado": "+56 9 1234 5678",
                "observaciones": "Estudiante muy participativa, necesita apoyo en matemáticas"
            },
            {
                "nombre": "Diego",
                "apellido": "Martínez",
                "curso": "1° Medio",
                "id_colegio": colegio_ids[1],
                "nombre_apoderado": "Carlos Martínez",
                "contacto_apoderado": "carlos.martinez@email.com",
                "observaciones": "Excelente rendimiento, líder natural del grupo"
            },
            {
                "nombre": "Sofía",
                "apellido": "López",
                "curso": "5° Básico",
                "id_colegio": colegio_ids[0],
                "nombre_apoderado": "Patricia López",
                "contacto_apoderado": "+56 9 8765 4321",
                "observaciones": "Necesita mejorar en lectura comprensiva"
            },
            {
                "nombre": "Sebastián",
                "apellido": "González",
                "curso": "2° Medio",
                "id_colegio": colegio_ids[1],
                "nombre_apoderado": "Roberto González",
                "contacto_apoderado": "roberto.gonzalez@email.com",
                "observaciones": "Interesado en ciencias, muy creativo"
            },
            {
                "nombre": "Valentina",
                "apellido": "Rodríguez",
                "curso": "4° Básico",
                "id_colegio": colegio_ids[0],
                "nombre_apoderado": "Carmen Rodríguez",
                "contacto_apoderado": "+56 9 5555 1234",
                "observaciones": "Buena asistencia, participa activamente"
            },
            {
                "nombre": "Matías",
                "apellido": "Herrera",
                "curso": "3° Medio",
                "id_colegio": colegio_ids[1],
                "nombre_apoderado": "Luis Herrera",
                "contacto_apoderado": "luis.herrera@email.com",
                "observaciones": "Necesita apoyo en inglés, muy motivado"
            },
            {
                "nombre": "Isabella",
                "apellido": "Vargas",
                "curso": "6° Básico",
                "id_colegio": colegio_ids[0],
                "nombre_apoderado": "Elena Vargas",
                "contacto_apoderado": "+56 9 3333 7777",
                "observaciones": "Excelente en artes, necesita apoyo en ciencias"
            },
            {
                "nombre": "Nicolás",
                "apellido": "Torres",
                "curso": "1° Básico",
                "id_colegio": colegio_ids[0],
                "nombre_apoderado": "Andrea Torres",
                "contacto_apoderado": "andrea.torres@email.com",
                "observaciones": "Primer año, muy entusiasta y colaborador"
            },
            {
                "nombre": "Camila",
                "apellido": "Morales",
                "curso": "2° Básico",
                "id_colegio": colegio_ids[1],
                "nombre_apoderado": "Pedro Morales",
                "contacto_apoderado": "+56 9 4444 8888",
                "observaciones": "Muy tímida, necesita confianza para participar"
            },
            {
                "nombre": "Joaquín",
                "apellido": "Castro",
                "curso": "4° Medio",
                "id_colegio": colegio_ids[1],
                "nombre_apoderado": "Rosa Castro",
                "contacto_apoderado": "rosa.castro@email.com",
                "observaciones": "Preparándose para PSU, muy dedicado"
            }
        ]
        
        for student_data in students_data:
            # Generar RUT único
            rut = generate_rut()
            while db.query(Student).filter(Student.rut == rut).first():
                rut = generate_rut()
            
            student = Student(
                rut=rut,
                nombre=student_data["nombre"],
                apellido=student_data["apellido"],
                curso=student_data["curso"],
                id_colegio=student_data["id_colegio"],
                nombre_apoderado=student_data["nombre_apoderado"],
                contacto_apoderado=student_data["contacto_apoderado"],
                observaciones=student_data["observaciones"]
            )
            
            db.add(student)
            print(f"  [OK] {student.nombre} {student.apellido} - RUT: {student.rut}")
        
        db.commit()
        
        # 5. Crear datos de asistencia usando el modelo nuevo
        print("\n5. Creando datos de asistencia...")
        all_students = db.query(Student).all()
        
        for student in all_students:
            for week_num in range(1, 11):
                week_key = f"semana_{week_num}"
                
                existing = db.query(StudentAttendance).filter(
                    StudentAttendance.id_estudiante == student.id,
                    StudentAttendance.semana == week_key
                ).first()
                
                if not existing:
                    # Generar asistencia aleatoria (70% de probabilidad de asistir)
                    attended = random.random() < 0.7
                    status = AttendanceStatus.ASISTIO if attended else AttendanceStatus.NO_ASISTIO
                    
                    attendance_record = StudentAttendance(
                        id_estudiante=student.id,
                        semana=week_key,
                        estado=status
                    )
                    db.add(attendance_record)
        
        db.commit()
        print(f"  [OK] Datos de asistencia creados para {len(all_students)} estudiantes")
        
        # 6. Mostrar resumen final
        print("\n=== RESUMEN DEL SISTEMA ===")
        schools_count = db.query(School).count()
        users_count = db.query(User).count()
        tutors_count = db.query(Tutor).count()
        students_count = db.query(Student).count()
        attendance_count = db.query(StudentAttendance).count()
        
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
            attendance_records = db.query(StudentAttendance).filter(
                StudentAttendance.id_estudiante == student.id
            ).all()
            
            attended_count = sum(1 for record in attendance_records if record.estado.value == "asistio")
            percentage = (attended_count / 10) * 100
            
            print(f"{student.nombre} {student.apellido} ({student.rut})")
            print(f"  Curso: {student.curso} | Asistencia: {attended_count}/10 ({percentage:.1f}%)")
            print(f"  Apoderado: {student.nombre_apoderado} | Contacto: {student.contacto_apoderado}")
            print()
        
        print("[SUCCESS] Sistema inicializado correctamente!")
        print("\nPara probar el sistema:")
        print("1. Ejecuta: uvicorn app.main:app --reload --port 8000")
        print("2. En otra terminal: npm run dev")
        print("3. Ve a http://localhost:5173 y haz login")
    
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_data_fixed()
