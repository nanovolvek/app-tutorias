#!/usr/bin/env python3
"""
Script para configurar variables de entorno de producción
"""

import os
import sys

def create_prod_env():
    """Crear archivo .env para producción"""
    print("Configurando variables de entorno para produccion...")
    
    # URL de la base de datos de producción (AWS RDS)
    # Esta es la URL que debería estar configurada en AWS App Runner
    prod_database_url = "postgresql://postgres:nanopostgres@tutorias-db.cqj8x9x9x9x9.us-east-1.rds.amazonaws.com:5432/tutorias_db"
    
    # Configuración de producción
    env_content = f"""# Configuración de producción - AWS
DATABASE_URL={prod_database_url}
SECRET_KEY=super-secret-key-for-production-aws-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://main.d1d2p1x4drhejl.amplifyapp.com,http://localhost:5173
APP_NAME=Plataforma Tutorías
APP_VERSION=2.0.0

# Configuración local para sincronización
LOCAL_DATABASE_URL=postgresql://postgres:nanopostgres@localhost:5432/tutorias_db
"""
    
    # Escribir archivo .env
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("Archivo .env creado para produccion")
    return True

def main():
    """Función principal"""
    print("CONFIGURANDO ENTORNO DE PRODUCCION")
    print("=" * 50)
    
    # Crear archivo .env
    if create_prod_env():
        print("Configuracion completada")
        print("")
        print("Proximos pasos:")
        print("1. Verificar que la URL de la base de datos sea correcta")
        print("2. Ejecutar: python run_prod_migrations.py")
        print("")
        print("NOTA: Si la URL de la base de datos no es correcta,")
        print("   actualiza el archivo .env con la URL correcta de AWS RDS")
        return True
    else:
        print("Error en la configuracion")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
