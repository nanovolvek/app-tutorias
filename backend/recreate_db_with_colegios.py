import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.auth.security import get_password_hash
from dotenv import load_dotenv

load_dotenv()

def recreate_db_with_colegios():
    """Recrea la base de datos con la nueva estructura de colegios"""
    print("Recreando base de datos con estructura de colegios...")
    
    try:
        # Eliminar todas las tablas
        print("Eliminando tablas existentes...")
        models.Base.metadata.drop_all(bind=engine)
        
        # Crear todas las tablas
        print("Creando nuevas tablas...")
        models.Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        
        try:
            print("Creando colegios...")
            # Crear colegios
            colegios_data = [
                {"nombre": "Colegio San Patricio", "comuna": "Las Condes"},
                {"nombre": "Liceo Manuel Barros Borgoño", "comuna": "Santiago"},
                {"nombre": "Instituto Nacional", "comuna": "Santiago"}
            ]
            
            colegios = []
            for col_data in colegios_data:
                colegio = models.Colegio(**col_data)
                db.add(colegio)
                colegios.append(colegio)
            
            db.commit()
            
            print("Creando equipos...")
            # Crear equipos A, B, C con colegios asignados
            equipos_data = [
                {"nombre": "A", "descripcion": "Equipo A - Tutores y estudiantes", "colegio_id": colegios[0].id},
                {"nombre": "B", "descripcion": "Equipo B - Tutores y estudiantes", "colegio_id": colegios[1].id},
                {"nombre": "C", "descripcion": "Equipo C - Tutores y estudiantes", "colegio_id": colegios[2].id}
            ]
            
            equipos = []
            for eq_data in equipos_data:
                equipo = models.Equipo(**eq_data)
                db.add(equipo)
                equipos.append(equipo)
            
            db.commit()
            
            print("Creando usuarios...")
            # Crear usuarios
            usuarios_data = [
                {
                    "email": "admin@tutorias.com",
                    "hashed_password": get_password_hash("admin123"),
                    "nombre_completo": "Administrador Sistema",
                    "rol": "admin",
                    "equipo_id": None
                },
                {
                    "email": "tutor1@tutorias.com",
                    "hashed_password": get_password_hash("tutor123"),
                    "nombre_completo": "Tutor Equipo A",
                    "rol": "tutor",
                    "equipo_id": equipos[0].id
                },
                {
                    "email": "tutor2@tutorias.com",
                    "hashed_password": get_password_hash("tutor123"),
                    "nombre_completo": "Tutor Equipo B",
                    "rol": "tutor",
                    "equipo_id": equipos[1].id
                }
            ]
            
            for user_data in usuarios_data:
                usuario = models.Usuario(**user_data)
                db.add(usuario)
            
            db.commit()
            
            print("Creando tutores...")
            # Crear tutores (2 por equipo)
            tutores_data = [
                # Equipo A
                {"nombre": "Ana", "apellido": "Garcia", "email": "ana.garcia@tutorias.com", "equipo_id": equipos[0].id},
                {"nombre": "Carlos", "apellido": "Lopez", "email": "carlos.lopez@tutorias.com", "equipo_id": equipos[0].id},
                # Equipo B
                {"nombre": "Maria", "apellido": "Rodriguez", "email": "maria.rodriguez@tutorias.com", "equipo_id": equipos[1].id},
                {"nombre": "Pedro", "apellido": "Martinez", "email": "pedro.martinez@tutorias.com", "equipo_id": equipos[1].id},
                # Equipo C
                {"nombre": "Laura", "apellido": "Sanchez", "email": "laura.sanchez@tutorias.com", "equipo_id": equipos[2].id},
                {"nombre": "Diego", "apellido": "Fernandez", "email": "diego.fernandez@tutorias.com", "equipo_id": equipos[2].id}
            ]
            
            for tutor_data in tutores_data:
                tutor = models.Tutor(**tutor_data)
                db.add(tutor)
            
            db.commit()
            
            print("Creando estudiantes...")
            # Crear estudiantes (5 por equipo)
            estudiantes_data = [
                # Equipo A
                {"rut": "12.345.678-9", "nombre": "Sofia", "apellido": "Silva", "curso": "3° Basico", "equipo_id": equipos[0].id, "nombre_apoderado": "Juan Silva", "contacto_apoderado": "juan.silva@email.com"},
                {"rut": "23.456.789-0", "nombre": "Mateo", "apellido": "Gonzalez", "curso": "3° Basico", "equipo_id": equipos[0].id, "nombre_apoderado": "Carmen Gonzalez", "contacto_apoderado": "carmen.gonzalez@email.com"},
                {"rut": "34.567.890-1", "nombre": "Isabella", "apellido": "Perez", "curso": "4° Basico", "equipo_id": equipos[0].id, "nombre_apoderado": "Roberto Perez", "contacto_apoderado": "roberto.perez@email.com"},
                {"rut": "45.678.901-2", "nombre": "Santiago", "apellido": "Hernandez", "curso": "4° Basico", "equipo_id": equipos[0].id, "nombre_apoderado": "Patricia Hernandez", "contacto_apoderado": "patricia.hernandez@email.com"},
                {"rut": "56.789.012-3", "nombre": "Valentina", "apellido": "Torres", "curso": "5° Basico", "equipo_id": equipos[0].id, "nombre_apoderado": "Miguel Torres", "contacto_apoderado": "miguel.torres@email.com"},
                
                # Equipo B
                {"rut": "67.890.123-4", "nombre": "Sebastian", "apellido": "Ramirez", "curso": "3° Basico", "equipo_id": equipos[1].id, "nombre_apoderado": "Elena Ramirez", "contacto_apoderado": "elena.ramirez@email.com"},
                {"rut": "78.901.234-5", "nombre": "Camila", "apellido": "Flores", "curso": "3° Basico", "equipo_id": equipos[1].id, "nombre_apoderado": "Andres Flores", "contacto_apoderado": "andres.flores@email.com"},
                {"rut": "89.012.345-6", "nombre": "Nicolas", "apellido": "Vargas", "curso": "4° Basico", "equipo_id": equipos[1].id, "nombre_apoderado": "Monica Vargas", "contacto_apoderado": "monica.vargas@email.com"},
                {"rut": "90.123.456-7", "nombre": "Antonella", "apellido": "Castro", "curso": "4° Basico", "equipo_id": equipos[1].id, "nombre_apoderado": "Fernando Castro", "contacto_apoderado": "fernando.castro@email.com"},
                {"rut": "01.234.567-8", "nombre": "Maximiliano", "apellido": "Morales", "curso": "5° Basico", "equipo_id": equipos[1].id, "nombre_apoderado": "Claudia Morales", "contacto_apoderado": "claudia.morales@email.com"},
                
                # Equipo C
                {"rut": "11.111.111-1", "nombre": "Emilia", "apellido": "Jimenez", "curso": "3° Basico", "equipo_id": equipos[2].id, "nombre_apoderado": "Ricardo Jimenez", "contacto_apoderado": "ricardo.jimenez@email.com"},
                {"rut": "22.222.222-2", "nombre": "Benjamin", "apellido": "Ruiz", "curso": "3° Basico", "equipo_id": equipos[2].id, "nombre_apoderado": "Alejandra Ruiz", "contacto_apoderado": "alejandra.ruiz@email.com"},
                {"rut": "33.333.333-3", "nombre": "Javiera", "apellido": "Mendoza", "curso": "4° Basico", "equipo_id": equipos[2].id, "nombre_apoderado": "Pablo Mendoza", "contacto_apoderado": "pablo.mendoza@email.com"},
                {"rut": "44.444.444-4", "nombre": "Agustin", "apellido": "Guerrero", "curso": "4° Basico", "equipo_id": equipos[2].id, "nombre_apoderado": "Silvia Guerrero", "contacto_apoderado": "silvia.guerrero@email.com"},
                {"rut": "55.555.555-5", "nombre": "Constanza", "apellido": "Rojas", "curso": "5° Basico", "equipo_id": equipos[2].id, "nombre_apoderado": "Hector Rojas", "contacto_apoderado": "hector.rojas@email.com"}
            ]
            
            for student_data in estudiantes_data:
                estudiante = models.Estudiante(**student_data)
                db.add(estudiante)
            
            db.commit()
            
            print("Inicializando datos de asistencia...")
            # Inicializar datos de asistencia
            from app.models.attendance import AsistenciaEstudiante, AsistenciaTutor, EstadoAsistencia
            import random
            
            # Crear datos de asistencia para estudiantes
            for estudiante in estudiantes_data:
                estudiante_obj = db.query(models.Estudiante).filter(
                    models.Estudiante.rut == estudiante["rut"]
                ).first()
                if estudiante_obj:
                    for week_num in range(1, 11):
                        week_key = f"semana_{week_num}"
                        # 70% de probabilidad de asistir
                        status = EstadoAsistencia.ASISTIO if random.random() < 0.7 else random.choice([
                            EstadoAsistencia.NO_ASISTIO, 
                            EstadoAsistencia.SUSPENDIDA, 
                            EstadoAsistencia.VACACIONES
                        ])
                        
                        attendance_record = AsistenciaEstudiante(
                            estudiante_id=estudiante_obj.id,
                            semana=week_key,
                            estado=status
                        )
                        db.add(attendance_record)
            
            # Crear datos de asistencia para tutores
            for tutor in tutores_data:
                tutor_obj = db.query(models.Tutor).filter(
                    models.Tutor.email == tutor["email"]
                ).first()
                if tutor_obj:
                    for week_num in range(1, 11):
                        week_key = f"semana_{week_num}"
                        # 80% de probabilidad de asistir (tutores más responsables)
                        status = EstadoAsistencia.ASISTIO if random.random() < 0.8 else random.choice([
                            EstadoAsistencia.NO_ASISTIO, 
                            EstadoAsistencia.SUSPENDIDA, 
                            EstadoAsistencia.VACACIONES
                        ])
                        
                        attendance_record = AsistenciaTutor(
                            tutor_id=tutor_obj.id,
                            semana=week_key,
                            estado=status
                        )
                        db.add(attendance_record)
            
            db.commit()
            
            print("Base de datos recreada correctamente!")
            print(f"   - 3 colegios")
            print(f"   - 3 equipos (A, B, C) con colegios asignados")
            print(f"   - 3 usuarios (1 admin, 2 tutores)")
            print(f"   - 6 tutores (2 por equipo)")
            print(f"   - 15 estudiantes (5 por equipo)")
            print(f"   - Datos de asistencia para 10 semanas")
            print("\nCredenciales de acceso:")
            print("   Admin: admin@tutorias.com / admin123")
            print("   Tutor Equipo A: tutor1@tutorias.com / tutor123")
            print("   Tutor Equipo B: tutor2@tutorias.com / tutor123")
            
            return True
            
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            db.rollback()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error de conexion a RDS: {e}")
        return False

if __name__ == "__main__":
    recreate_db_with_colegios()
