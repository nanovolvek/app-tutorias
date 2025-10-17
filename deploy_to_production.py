#!/usr/bin/env python3
"""
Script de despliegue completo a producción
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"   Salida: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

def check_git_status():
    """Verificar estado de git"""
    print("🔍 Verificando estado de git...")
    
    # Verificar si hay cambios sin commitear
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("⚠️  Hay cambios sin commitear:")
        print(result.stdout)
        response = input("¿Deseas continuar? (y/N): ")
        if response.lower() != 'y':
            print("❌ Despliegue cancelado")
            return False
    
    # Verificar rama actual
    result = subprocess.run("git branch --show-current", shell=True, capture_output=True, text=True)
    current_branch = result.stdout.strip()
    print(f"📍 Rama actual: {current_branch}")
    
    if current_branch != 'main':
        print("⚠️  No estás en la rama main")
        response = input("¿Deseas cambiar a main? (y/N): ")
        if response.lower() == 'y':
            if not run_command("git checkout main", "Cambiando a rama main"):
                return False
        else:
            print("❌ Despliegue cancelado")
            return False
    
    return True

def build_frontend():
    """Construir frontend para producción"""
    print("🏗️  Construyendo frontend...")
    
    # Instalar dependencias
    if not run_command("npm install", "Instalando dependencias de frontend"):
        return False
    
    # Construir para producción
    if not run_command("npm run build", "Construyendo frontend para producción"):
        return False
    
    return True

def commit_changes():
    """Commitear todos los cambios"""
    print("📝 Commiteando cambios...")
    
    # Agregar todos los archivos
    if not run_command("git add .", "Agregando archivos al staging"):
        return False
    
    # Commit con mensaje descriptivo
    commit_message = "feat: Despliegue completo con nuevas funcionalidades de gestión de estudiantes y tutores"
    if not run_command(f'git commit -m "{commit_message}"', "Commiteando cambios"):
        return False
    
    return True

def push_to_production():
    """Subir cambios a producción"""
    print("🚀 Subiendo a producción...")
    
    # Push a main
    if not run_command("git push origin main", "Subiendo cambios a main"):
        return False
    
    print("✅ Código subido a producción")
    print("🔄 AWS App Runner iniciará el despliegue automático...")
    
    return True

def main():
    """Función principal de despliegue"""
    print("🚀 INICIANDO DESPLIEGUE A PRODUCCIÓN")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path("package.json").exists() or not Path("backend").exists():
        print("❌ Error: No estás en el directorio raíz del proyecto")
        return False
    
    # Paso 1: Verificar git
    if not check_git_status():
        return False
    
    # Paso 2: Construir frontend
    if not build_frontend():
        return False
    
    # Paso 3: Commitear cambios
    if not commit_changes():
        return False
    
    # Paso 4: Subir a producción
    if not push_to_production():
        return False
    
    print("=" * 50)
    print("🎉 DESPLIEGUE COMPLETADO EXITOSAMENTE!")
    print("")
    print("📋 Próximos pasos:")
    print("1. Esperar 5-10 minutos para que AWS App Runner complete el despliegue")
    print("2. Verificar que la aplicación funcione en:")
    print("   - Frontend: https://main.d1d2p1x4drhejl.amplifyapp.com")
    print("   - Backend: https://wh7jum5qhe.us-east-1.awsapprunner.com")
    print("3. Ejecutar migraciones de base de datos si es necesario")
    print("")
    print("⚠️  IMPORTANTE: Si hay cambios en la base de datos,")
    print("   ejecuta el script de migración en producción:")
    print("   python backend/migrate_prod_database.py")
    print("   python backend/sync_local_to_prod.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
