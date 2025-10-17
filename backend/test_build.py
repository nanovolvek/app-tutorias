#!/usr/bin/env python3
"""
Script para probar que el build funcione correctamente
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Probar que todas las importaciones funcionen"""
    print("Probando importaciones...")
    
    try:
        from app.main import app
        print("OK: app.main importado correctamente")
    except Exception as e:
        print(f"ERROR: Error importando app.main: {e}")
        return False
    
    try:
        from app.routers import attendance
        print("OK: app.routers.attendance importado correctamente")
    except Exception as e:
        print(f"ERROR: Error importando attendance: {e}")
        return False
    
    try:
        from app.routers import tutor_attendance
        print("OK: app.routers.tutor_attendance importado correctamente")
    except Exception as e:
        print(f"ERROR: Error importando tutor_attendance: {e}")
        return False
    
    try:
        from app.models.attendance import AsistenciaEstudiante, AsistenciaTutor, EstadoAsistencia
        print("OK: Modelos de asistencia importados correctamente")
    except Exception as e:
        print(f"ERROR: Error importando modelos de asistencia: {e}")
        return False
    
    return True

def test_routes():
    """Probar que las rutas estén registradas"""
    print("\nProbando rutas...")
    
    try:
        from app.main import app
        
        # Obtener todas las rutas
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        # Buscar rutas de asistencia
        attendance_routes = [route for route in routes if 'attendance' in route]
        
        if attendance_routes:
            print("OK: Rutas de asistencia encontradas:")
            for route in attendance_routes:
                print(f"  - {route}")
        else:
            print("ERROR: No se encontraron rutas de asistencia")
            print("Rutas disponibles:")
            for route in sorted(routes):
                print(f"  - {route}")
            return False
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error probando rutas: {e}")
        return False

def main():
    """Función principal"""
    print("=== PROBANDO BUILD LOCAL ===")
    
    if not test_imports():
        print("\nERROR: Falló la prueba de importaciones")
        return False
    
    if not test_routes():
        print("\nERROR: Falló la prueba de rutas")
        return False
    
    print("\nOK: Todas las pruebas pasaron - el build local funciona correctamente")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
