#!/usr/bin/env python3
"""
Script para ejecutar migraciones de Alembic y crear la tabla de asistencia
"""

import subprocess
import sys
import os

def run_migration():
    """Ejecutar migración de Alembic"""
    try:
        # Cambiar al directorio backend
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        print("Ejecutando migración de Alembic...")
        
        # Crear nueva migración
        result = subprocess.run([
            "alembic", "revision", "--autogenerate", "-m", "Add attendance table and student fields"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error creando migración: {result.stderr}")
            return False
        
        print("Migración creada exitosamente")
        
        # Aplicar migración
        result = subprocess.run([
            "alembic", "upgrade", "head"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error aplicando migración: {result.stderr}")
            return False
        
        print("Migración aplicada exitosamente")
        return True
        
    except Exception as e:
        print(f"Error ejecutando migración: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    if success:
        print("Migración completada exitosamente")
    else:
        print("Error en la migración")
        sys.exit(1)
