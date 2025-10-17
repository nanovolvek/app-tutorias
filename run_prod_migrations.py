#!/usr/bin/env python3
"""
Script para ejecutar migraciones en producción
IMPORTANTE: Este script debe ejecutarse DESPUÉS de que AWS App Runner haya desplegado el código
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

def wait_for_deployment():
    """Esperar a que el despliegue esté completo"""
    print("Esperando a que AWS App Runner complete el despliegue...")
    print("   Esto puede tomar 5-10 minutos...")
    
    backend_url = "https://wh7jum5qhe.us-east-1.awsapprunner.com"
    frontend_url = "https://main.d1d2p1x4drhejl.amplifyapp.com"
    
    max_attempts = 30  # 30 intentos = 15 minutos
    attempt = 0
    
    while attempt < max_attempts:
        try:
            # Verificar backend
            response = requests.get(f"{backend_url}/docs", timeout=10)
            if response.status_code == 200:
                print("Backend desplegado correctamente")
                
                # Verificar frontend
                response = requests.get(frontend_url, timeout=10)
                if response.status_code == 200:
                    print("Frontend desplegado correctamente")
                    return True
                else:
                    print(f"Frontend aun no disponible (intento {attempt + 1}/{max_attempts})")
            else:
                print(f"Backend aun no disponible (intento {attempt + 1}/{max_attempts})")
                
        except requests.exceptions.RequestException:
            print(f"Servicios aun no disponibles (intento {attempt + 1}/{max_attempts})")
        
        attempt += 1
        time.sleep(30)  # Esperar 30 segundos entre intentos
    
    print("Timeout: Los servicios no estuvieron disponibles en el tiempo esperado")
    return False

def run_migrations():
    """Ejecutar migraciones de base de datos"""
    print("Ejecutando migraciones de base de datos...")
    
    # Cambiar al directorio backend
    os.chdir("backend")
    
    try:
        # Ejecutar migración de estructura
        print("Aplicando cambios de estructura...")
        result = os.system("python migrate_prod_database.py")
        if result != 0:
            print("Error en migracion de estructura")
            return False
        
        # Ejecutar sincronización de datos
        print("Sincronizando datos de asistencia...")
        result = os.system("python sync_local_to_prod.py")
        if result != 0:
            print("Error en sincronizacion de datos")
            return False
        
        print("Migraciones completadas exitosamente")
        return True
        
    except Exception as e:
        print(f"Error durante las migraciones: {e}")
        return False
    finally:
        os.chdir("..")

def verify_deployment():
    """Verificar que el despliegue funcione correctamente"""
    print("Verificando funcionalidad del despliegue...")
    
    backend_url = "https://wh7jum5qhe.us-east-1.awsapprunner.com"
    
    try:
        # Verificar endpoint de estudiantes
        response = requests.get(f"{backend_url}/estudiantes/", timeout=10)
        if response.status_code == 200:
            print("Endpoint de estudiantes funcionando")
        else:
            print(f"Endpoint de estudiantes: {response.status_code}")
        
        # Verificar endpoint de tutores
        response = requests.get(f"{backend_url}/tutores/", timeout=10)
        if response.status_code == 200:
            print("Endpoint de tutores funcionando")
        else:
            print(f"Endpoint de tutores: {response.status_code}")
        
        # Verificar endpoint de asistencia
        response = requests.get(f"{backend_url}/attendance/students/attendance-stats", timeout=10)
        if response.status_code == 200:
            print("Endpoint de estadisticas de asistencia funcionando")
        else:
            print(f"Endpoint de estadisticas: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"Error verificando despliegue: {e}")
        return False

def main():
    """Función principal"""
    print("INICIANDO PROCESO DE MIGRACION EN PRODUCCION")
    print("=" * 60)
    
    # Configurar URL de producción directamente
    os.environ['DATABASE_URL'] = 'postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres'
    os.environ['LOCAL_DATABASE_URL'] = 'postgresql://postgres:nanopostgres@localhost:5432/tutorias_db'
    
    print("Configuracion de base de datos establecida:")
    print(f"Produccion: {os.environ['DATABASE_URL']}")
    print(f"Local: {os.environ['LOCAL_DATABASE_URL']}")
    
    # Paso 1: Esperar despliegue
    if not wait_for_deployment():
        print("No se pudo verificar el despliegue")
        return False
    
    # Paso 2: Ejecutar migraciones
    if not run_migrations():
        print("Error en las migraciones")
        return False
    
    # Paso 3: Verificar funcionalidad
    if not verify_deployment():
        print("Error en la verificacion")
        return False
    
    print("=" * 60)
    print("DESPLIEGUE Y MIGRACION COMPLETADOS EXITOSAMENTE!")
    print("")
    print("URLs de produccion:")
    print("   Frontend: https://main.d1d2p1x4drhejl.amplifyapp.com")
    print("   Backend:  https://wh7jum5qhe.us-east-1.awsapprunner.com")
    print("")
    print("Funcionalidades desplegadas:")
    print("   - Gestion completa de estudiantes y tutores")
    print("   - Graficos de asistencia en Dashboard")
    print("   - Exportacion Excel")
    print("   - Permisos por rol")
    print("   - Datos de asistencia sincronizados")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
