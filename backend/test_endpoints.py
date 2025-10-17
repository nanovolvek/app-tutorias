#!/usr/bin/env python3
"""
Script para probar los endpoints de la API
"""

import requests
import json

def test_endpoints():
    """Probar los endpoints de la API"""
    base_url = "https://wh7jum5qhe.us-east-1.awsapprunner.com"
    
    print("Probando endpoints de la API...")
    
    # 1. Probar endpoint de estudiantes
    print("\n1. Probando endpoint de estudiantes...")
    try:
        response = requests.get(f"{base_url}/estudiantes/", timeout=10)
        if response.status_code == 200:
            estudiantes = response.json()
            print(f"Endpoint estudiantes funcionando - {len(estudiantes)} estudiantes")
            
            # Mostrar muestra de datos
            if estudiantes:
                print("Muestra de datos de estudiantes:")
                for i, est in enumerate(estudiantes[:3]):
                    equipo_nombre = est.get('equipo', {}).get('nombre', 'Sin equipo') if est.get('equipo') else 'Sin equipo'
                    colegio_nombre = est.get('equipo', {}).get('colegio', {}).get('nombre', 'Sin colegio') if est.get('equipo', {}).get('colegio') else 'Sin colegio'
                    print(f"  {est['nombre']} {est['apellido']} -> {equipo_nombre} -> {colegio_nombre}")
        else:
            print(f"Error en endpoint estudiantes: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"Error conectando a endpoint estudiantes: {e}")
    
    # 2. Probar endpoint de tutores
    print("\n2. Probando endpoint de tutores...")
    try:
        response = requests.get(f"{base_url}/tutores/", timeout=10)
        if response.status_code == 200:
            tutores = response.json()
            print(f"Endpoint tutores funcionando - {len(tutores)} tutores")
            
            # Mostrar muestra de datos
            if tutores:
                print("Muestra de datos de tutores:")
                for i, tut in enumerate(tutores[:3]):
                    equipo_nombre = tut.get('equipo', {}).get('nombre', 'Sin equipo') if tut.get('equipo') else 'Sin equipo'
                    colegio_nombre = tut.get('equipo', {}).get('colegio', {}).get('nombre', 'Sin colegio') if tut.get('equipo', {}).get('colegio') else 'Sin colegio'
                    print(f"  {tut['nombre']} {tut['apellido']} -> {equipo_nombre} -> {colegio_nombre}")
        else:
            print(f"Error en endpoint tutores: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"Error conectando a endpoint tutores: {e}")
    
    # 3. Probar endpoint de estadísticas de asistencia
    print("\n3. Probando endpoint de estadísticas de asistencia...")
    try:
        response = requests.get(f"{base_url}/attendance/students/attendance-stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print("Endpoint estadisticas funcionando")
            print(f"   Promedio general: {stats.get('average_attendance', 'N/A')}%")
            print(f"   Total estudiantes: {len(stats.get('student_attendance', []))}")
        else:
            print(f"Error en endpoint estadisticas: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"Error conectando a endpoint estadisticas: {e}")
    
    # 4. Probar endpoint de equipos
    print("\n4. Probando endpoint de equipos...")
    try:
        response = requests.get(f"{base_url}/equipos/", timeout=10)
        if response.status_code == 200:
            equipos = response.json()
            print(f"Endpoint equipos funcionando - {len(equipos)} equipos")
            
            # Mostrar muestra de datos
            if equipos:
                print("Muestra de datos de equipos:")
                for eq in equipos:
                    colegio_nombre = eq.get('colegio', {}).get('nombre', 'Sin colegio') if eq.get('colegio') else 'Sin colegio'
                    print(f"  {eq['nombre']} -> {colegio_nombre}")
        else:
            print(f"Error en endpoint equipos: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"Error conectando a endpoint equipos: {e}")

def main():
    """Función principal"""
    print("PROBANDO ENDPOINTS DE LA API")
    print("=" * 50)
    
    test_endpoints()
    
    print("\n" + "=" * 50)
    print("Prueba completada!")
    print("Si todos los endpoints muestran datos correctos,")
    print("la aplicación en producción debería funcionar correctamente.")

if __name__ == "__main__":
    main()