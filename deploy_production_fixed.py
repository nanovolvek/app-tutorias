#!/usr/bin/env python3
"""
Script para hacer deploy de la aplicación con correcciones de asistencia
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Iniciando deploy de producción con correcciones...")
    
    # 1. Construir frontend
    if not run_command("npm run build", "Construyendo frontend"):
        return False
    
    # 2. Verificar que el build se creó
    if not os.path.exists("dist"):
        print("❌ El directorio dist no existe. El build falló.")
        return False
    
    print("✅ Frontend construido correctamente")
    print("\n📋 Próximos pasos manuales:")
    print("1. Subir el código a GitHub")
    print("2. En AWS App Runner, actualizar la aplicación")
    print("3. En AWS Amplify, hacer redeploy del frontend")
    print("4. Configurar la variable de entorno VITE_API_URL en Amplify")
    print("5. Ejecutar el script de corrección de datos en producción:")
    print("   python backend/fix_production_data.py")
    
    print("\n🎉 Deploy preparado correctamente!")

if __name__ == "__main__":
    main()
