#!/usr/bin/env python3
"""
Script para arreglar los estudiantes que tienen RUT nulo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Student
import random

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

def fix_students_rut():
    """Arreglar estudiantes que tienen RUT nulo"""
    db = SessionLocal()
    
    try:
        print("Buscando estudiantes con RUT nulo...")
        
        # Buscar estudiantes con RUT nulo
        students_without_rut = db.query(Student).filter(Student.rut.is_(None)).all()
        
        if not students_without_rut:
            print("No hay estudiantes con RUT nulo.")
            return True
        
        print(f"Encontrados {len(students_without_rut)} estudiantes sin RUT")
        
        # Generar RUTs únicos para cada estudiante
        for student in students_without_rut:
            # Generar RUT único
            rut = generate_rut()
            while db.query(Student).filter(Student.rut == rut).first():
                rut = generate_rut()
            
            # Actualizar el estudiante
            student.rut = rut
            print(f"Actualizado: {student.first_name} {student.last_name} - RUT: {rut}")
        
        # Commit los cambios
        db.commit()
        print(f"Se actualizaron {len(students_without_rut)} estudiantes exitosamente")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = fix_students_rut()
    if success:
        print("Corrección completada exitosamente")
    else:
        print("Error en la corrección")
        sys.exit(1)
