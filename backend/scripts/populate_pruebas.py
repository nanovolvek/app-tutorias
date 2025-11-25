"""
Script para poblar datos de prueba para Prueba Diagnóstico y Prueba Unidad
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base
from app.models.prueba_diagnostico import PruebaDiagnosticoEstudiante, PorcentajeLogro as PorcentajeLogroDiagnostico
from app.models.prueba_unidad import PruebaUnidadEstudiante, PorcentajeLogro as PorcentajeLogroUnidad
from app.models.student import Estudiante
import random

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

def populate_pruebas():
    db: Session = SessionLocal()
    
    try:
        # Obtener todos los estudiantes
        estudiantes = db.query(Estudiante).all()
        
        if not estudiantes:
            print("No hay estudiantes en la base de datos. Por favor, crea estudiantes primero.")
            return
        
        print(f"Encontrados {len(estudiantes)} estudiantes")
        
        # Unidades y módulos disponibles
        unidades = ["unidad_1", "unidad_2", "unidad_3", "unidad_4", "unidad_5"]
        modulos_por_unidad = {
            "unidad_1": ["modulo_1", "modulo_2", "modulo_3", "modulo_4", "modulo_5"],
            "unidad_2": ["modulo_1", "modulo_2", "modulo_3", "modulo_4", "modulo_5"],
            "unidad_3": ["modulo_1", "modulo_2", "modulo_3", "modulo_4", "modulo_5", "modulo_6", "modulo_7", "modulo_8", "modulo_9", "modulo_10"],
            "unidad_4": ["modulo_1", "modulo_2", "modulo_3", "modulo_4", "modulo_5"],
            "unidad_5": ["modulo_1", "modulo_2", "modulo_3", "modulo_4", "modulo_5", "modulo_6", "modulo_7", "modulo_8"]
        }
        
        # Porcentajes disponibles
        porcentajes = ["0%", "20%", "40%", "60%", "80%", "100%"]
        
        # Contadores
        pruebas_diagnostico_creadas = 0
        pruebas_unidad_creadas = 0
        
        # Crear pruebas para cada estudiante
        for estudiante in estudiantes:
            # Crear algunas pruebas de diagnóstico (aleatorias)
            for unidad in unidades[:3]:  # Solo primeras 3 unidades para no saturar
                modulos = modulos_por_unidad[unidad]
                for modulo in modulos[:3]:  # Solo primeros 3 módulos
                    # Verificar si ya existe
                    existe = db.query(PruebaDiagnosticoEstudiante).filter(
                        PruebaDiagnosticoEstudiante.estudiante_id == estudiante.id,
                        PruebaDiagnosticoEstudiante.unidad == unidad,
                        PruebaDiagnosticoEstudiante.modulo == modulo
                    ).first()
                    
                    if not existe:
                        porcentaje = random.choice(porcentajes + ["vacío"])
                        prueba = PruebaDiagnosticoEstudiante(
                            estudiante_id=estudiante.id,
                            unidad=unidad,
                            modulo=modulo,
                            resultado=PorcentajeLogroDiagnostico(porcentaje)
                        )
                        db.add(prueba)
                        pruebas_diagnostico_creadas += 1
            
            # Crear algunas pruebas de unidad (aleatorias)
            for unidad in unidades[:2]:  # Solo primeras 2 unidades
                modulos = modulos_por_unidad[unidad]
                for modulo in modulos[:2]:  # Solo primeros 2 módulos
                    # Verificar si ya existe
                    existe = db.query(PruebaUnidadEstudiante).filter(
                        PruebaUnidadEstudiante.estudiante_id == estudiante.id,
                        PruebaUnidadEstudiante.unidad == unidad,
                        PruebaUnidadEstudiante.modulo == modulo
                    ).first()
                    
                    if not existe:
                        porcentaje = random.choice(porcentajes + ["vacío"])
                        prueba = PruebaUnidadEstudiante(
                            estudiante_id=estudiante.id,
                            unidad=unidad,
                            modulo=modulo,
                            resultado=PorcentajeLogroUnidad(porcentaje)
                        )
                        db.add(prueba)
                        pruebas_unidad_creadas += 1
        
        db.commit()
        
        print(f"Pruebas de diagnostico creadas: {pruebas_diagnostico_creadas}")
        print(f"Pruebas de unidad creadas: {pruebas_unidad_creadas}")
        print("Datos de prueba poblados exitosamente")
        
    except Exception as e:
        db.rollback()
        print(f"Error al poblar datos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    populate_pruebas()

