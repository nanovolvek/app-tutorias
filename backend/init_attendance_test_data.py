#!/usr/bin/env python3
"""
Script para crear datos de prueba de asistencia para estudiantes y tutores
Genera datos para las semanas 1-10 con estados aleatorios
"""

import sys
import os
import random
from datetime import datetime

# Agregar el directorio del backend al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.attendance import AsistenciaEstudiante, AsistenciaTutor, EstadoAsistencia
from app.models.student import Estudiante
from app.models.tutor import Tutor

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def create_attendance_test_data():
    """Crear datos de prueba de asistencia"""
    db = get_db()
    
    try:
        # Obtener todos los estudiantes
        estudiantes = db.query(Estudiante).all()
        print(f"Encontrados {len(estudiantes)} estudiantes")
        
        # Obtener todos los tutores
        tutores = db.query(Tutor).all()
        print(f"Encontrados {len(tutores)} tutores")
        
        if not estudiantes:
            print("No hay estudiantes en la base de datos. Ejecuta primero init_db.py")
            return
        
        if not tutores:
            print("No hay tutores en la base de datos. Ejecuta primero init_db.py")
            return
        
        # Estados posibles
        estados = [
            EstadoAsistencia.ASISTIO,
            EstadoAsistencia.NO_ASISTIO,
            EstadoAsistencia.SUSPENDIDA,
            EstadoAsistencia.VACACIONES
        ]
        
        # Probabilidades para cada estado (más realista)
        # 70% asistió, 20% no asistió, 5% suspendida, 5% vacaciones
        probabilidades = [0.70, 0.20, 0.05, 0.05]
        
        # Generar datos para estudiantes (semanas 1-10)
        print("Generando datos de asistencia para estudiantes...")
        for estudiante in estudiantes:
            for semana in range(1, 11):
                semana_str = f"semana_{semana}"
                
                # Verificar si ya existe el registro
                existing = db.query(AsistenciaEstudiante).filter(
                    AsistenciaEstudiante.estudiante_id == estudiante.id,
                    AsistenciaEstudiante.semana == semana_str
                ).first()
                
                if not existing:
                    # Seleccionar estado basado en probabilidades
                    estado = random.choices(estados, weights=probabilidades)[0]
                    
                    asistencia = AsistenciaEstudiante(
                        estudiante_id=estudiante.id,
                        semana=semana_str,
                        estado=estado
                    )
                    db.add(asistencia)
        
        # Generar datos para tutores (semanas 1-10)
        print("Generando datos de asistencia para tutores...")
        for tutor in tutores:
            for semana in range(1, 11):
                semana_str = f"semana_{semana}"
                
                # Verificar si ya existe el registro
                existing = db.query(AsistenciaTutor).filter(
                    AsistenciaTutor.tutor_id == tutor.id,
                    AsistenciaTutor.semana == semana_str
                ).first()
                
                if not existing:
                    # Los tutores tienen mejor asistencia: 85% asistió, 10% no asistió, 3% suspendida, 2% vacaciones
                    tutor_probabilidades = [0.85, 0.10, 0.03, 0.02]
                    estado = random.choices(estados, weights=tutor_probabilidades)[0]
                    
                    asistencia = AsistenciaTutor(
                        tutor_id=tutor.id,
                        semana=semana_str,
                        estado=estado
                    )
                    db.add(asistencia)
        
        # Confirmar cambios
        db.commit()
        print("Datos de asistencia creados exitosamente!")
        
        # Mostrar resumen
        total_estudiantes = db.query(AsistenciaEstudiante).count()
        total_tutores = db.query(AsistenciaTutor).count()
        print(f"Total registros de asistencia de estudiantes: {total_estudiantes}")
        print(f"Total registros de asistencia de tutores: {total_tutores}")
        
        # Mostrar algunos ejemplos
        print("\nEjemplos de datos creados:")
        print("Estudiantes:")
        for i, asistencia in enumerate(db.query(AsistenciaEstudiante).limit(5).all()):
            estudiante = db.query(Estudiante).filter(Estudiante.id == asistencia.estudiante_id).first()
            print(f"  {estudiante.nombre} {estudiante.apellido} - {asistencia.semana}: {asistencia.estado.value}")
        
        print("Tutores:")
        for i, asistencia in enumerate(db.query(AsistenciaTutor).limit(5).all()):
            tutor = db.query(Tutor).filter(Tutor.id == asistencia.tutor_id).first()
            print(f"  {tutor.nombre} {tutor.apellido} - {asistencia.semana}: {asistencia.estado.value}")
            
    except Exception as e:
        print(f"Error al crear datos de asistencia: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Iniciando creacion de datos de prueba de asistencia...")
    create_attendance_test_data()
    print("Proceso completado!")
