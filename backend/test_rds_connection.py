import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_rds_connection():
    """Probar conexión a RDS"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("ERROR: DATABASE_URL no esta configurada")
        return False
    
    print(f"Probando conexion a: {database_url}")
    
    try:
        # Extraer componentes de la URL
        # postgresql://postgres:password@host:port/database
        parts = database_url.replace("postgresql://", "").split("@")
        if len(parts) != 2:
            print("ERROR: Formato de DATABASE_URL invalido")
            return False
            
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
        
        # Intentar conexión
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            connect_timeout=10
        )
        
        print("SUCCESS: Conexion exitosa a RDS!")
        
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
        return False

if __name__ == "__main__":
    test_rds_connection()
