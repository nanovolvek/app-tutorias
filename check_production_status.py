#!/usr/bin/env python3
"""
Script para verificar el estado de la aplicación en producción
"""

import requests
import json
import time

def check_production_status():
    """Verificar el estado de la aplicación en producción"""
    
    base_url = "https://wh7jum5qhe.us-east-1.awsapprunner.com"
    
    print("=== VERIFICANDO ESTADO DE PRODUCCION ===")
    
    # 1. Verificar health check
    print("\n1. Verificando health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("OK: Health check funcionando")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"ERROR: Health check falló con código {response.status_code}")
    except Exception as e:
        print(f"ERROR: No se puede conectar al health check: {e}")
        return False
    
    # 2. Verificar endpoints disponibles
    print("\n2. Verificando endpoints disponibles...")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=10)
        if response.status_code == 200:
            openapi = response.json()
            paths = openapi.get("paths", {})
            
            # Buscar endpoints de asistencia
            attendance_endpoints = [path for path in paths.keys() if "attendance" in path]
            if attendance_endpoints:
                print("OK: Endpoints de asistencia encontrados:")
                for endpoint in attendance_endpoints:
                    print(f"   - {endpoint}")
            else:
                print("ERROR: No se encontraron endpoints de asistencia")
                print("Endpoints disponibles:")
                for path in sorted(paths.keys()):
                    print(f"   - {path}")
        else:
            print(f"ERROR: No se puede obtener OpenAPI con código {response.status_code}")
    except Exception as e:
        print(f"ERROR: Error al verificar endpoints: {e}")
        return False
    
    # 3. Verificar endpoint específico de asistencia
    print("\n3. Verificando endpoint de estadísticas de asistencia...")
    try:
        response = requests.get(f"{base_url}/attendance/students/attendance-stats", timeout=10)
        if response.status_code == 200:
            print("OK: Endpoint de estadísticas de asistencia funcionando")
            data = response.json()
            print(f"   Datos recibidos: {len(data.get('students_stats', []))} estudiantes")
        elif response.status_code == 404:
            print("ERROR: Endpoint no encontrado (404)")
        else:
            print(f"ERROR: Endpoint falló con código {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"ERROR: Error al verificar endpoint de asistencia: {e}")
    
    print("\n=== VERIFICACION COMPLETADA ===")
    return True

if __name__ == "__main__":
    check_production_status()
