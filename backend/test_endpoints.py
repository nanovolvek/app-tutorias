#!/usr/bin/env python3
"""
Script para probar los endpoints del backend
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import json

def test_endpoints():
    """Probar los endpoints del backend"""
    base_url = "http://localhost:8000"
    
    try:
        # 1. Probar endpoint de login
        print("1. Probando login...")
        login_data = {
            "username": "admin@tutorias.com",
            "password": "admin123"
        }
        
        response = requests.post(f"{base_url}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"   ✓ Login exitoso. Token obtenido.")
        else:
            print(f"   ✗ Error en login: {response.status_code} - {response.text}")
            return False
        
        # 2. Probar endpoint de estudiantes
        print("\n2. Probando endpoint de estudiantes...")
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(f"{base_url}/students/", headers=headers)
        if response.status_code == 200:
            students = response.json()
            print(f"   ✓ Endpoint de estudiantes funcionando. {len(students)} estudiantes encontrados.")
            
            # Mostrar algunos estudiantes
            for i, student in enumerate(students[:3]):
                print(f"   - {student['first_name']} {student['last_name']} (RUT: {student['rut']})")
        else:
            print(f"   ✗ Error en estudiantes: {response.status_code} - {response.text}")
            return False
        
        # 3. Probar endpoint de asistencia
        print("\n3. Probando endpoint de asistencia...")
        response = requests.get(f"{base_url}/attendance/summary", headers=headers)
        if response.status_code == 200:
            attendance = response.json()
            print(f"   ✓ Endpoint de asistencia funcionando. {len(attendance)} registros encontrados.")
        else:
            print(f"   ✗ Error en asistencia: {response.status_code} - {response.text}")
            return False
        
        print("\n✅ Todos los endpoints están funcionando correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_endpoints()
    if not success:
        sys.exit(1)
