import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_app_runner_rds():
    """Probar conexión desde App Runner a RDS"""
    
    # URL de RDS para App Runner
    rds_url = "postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres"
    
    print("Probando conexion desde App Runner a RDS...")
    print(f"URL: {rds_url}")
    
    try:
        # Extraer componentes de la URL
        parts = rds_url.replace("postgresql://", "").split("@")
        auth_part = parts[0]
        host_part = parts[1]
        
        user, password = auth_part.split(":")
        host_port_db = host_part.split("/")
        host_port = host_port_db[0].split(":")
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 5432
        database = host_port_db[1] if len(host_port_db) > 1 else "postgres"
        
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Database: {database}")
        print(f"   User: {user}")
        
        # Intentar conexión con timeout más largo
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            connect_timeout=30
        )
        
        print("SUCCESS: Conexion exitosa desde App Runner a RDS!")
        
        # Probar una consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error de conexion: {e}")
        print("\nPosibles soluciones:")
        print("1. Verificar que RDS tenga 'Public access: Yes'")
        print("2. Verificar que el Security Group permita conexiones en puerto 5432")
        print("3. Verificar que App Runner esté en la misma VPC o tenga acceso a RDS")
        return False

if __name__ == "__main__":
    test_app_runner_rds()
