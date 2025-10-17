"""
Script para sincronizar datos de producción (AWS RDS) a base de datos local
"""
import psycopg2
import json
from datetime import datetime

# Configuración de bases de datos
PROD_DB_URL = "postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres"
LOCAL_DB_URL = "postgresql://postgres:nanopostgres@localhost:5432/tutorias_db"

def get_connection(url):
    """Crear conexión a la base de datos"""
    return psycopg2.connect(url)

def clear_local_tables(local_conn):
    """Limpiar todas las tablas locales"""
    print("Limpiando tablas locales...")
    local_cur = local_conn.cursor()
    
    # Orden de eliminación para respetar foreign keys
    tables_to_clear = [
        'asistencia_estudiantes',
        'asistencia_tutores', 
        'estudiantes',
        'tutores',
        'usuarios',
        'equipos',
        'colegios'
    ]
    
    for table in tables_to_clear:
        try:
            local_cur.execute(f"DELETE FROM {table};")
            print(f"  OK - Limpiada tabla: {table}")
        except Exception as e:
            print(f"  ERROR - Error limpiando {table}: {e}")
    
    local_conn.commit()
    local_cur.close()

def sync_table(prod_conn, local_conn, table_name, columns):
    """Sincronizar una tabla específica"""
    print(f"Sincronizando tabla: {table_name}")
    
    prod_cur = prod_conn.cursor()
    local_cur = local_conn.cursor()
    
    try:
        # Obtener datos de producción
        prod_cur.execute(f"SELECT {', '.join(columns)} FROM {table_name};")
        rows = prod_cur.fetchall()
        
        if not rows:
            print(f"  WARNING - No hay datos en {table_name}")
            return
        
        # Insertar en local
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});"
        
        local_cur.executemany(insert_query, rows)
        local_conn.commit()
        
        print(f"  OK - Sincronizados {len(rows)} registros en {table_name}")
        
    except Exception as e:
        print(f"  ERROR - Error sincronizando {table_name}: {e}")
        local_conn.rollback()
    finally:
        prod_cur.close()
        local_cur.close()

def sync_database():
    """Sincronizar toda la base de datos"""
    print("INICIANDO SINCRONIZACION DE PRODUCCION A LOCAL")
    print("=" * 60)
    
    prod_conn = None
    local_conn = None
    
    try:
        # Conectar a ambas bases de datos
        print("Conectando a base de datos de produccion...")
        prod_conn = get_connection(PROD_DB_URL)
        print("OK - Conectado a produccion")
        
        print("Conectando a base de datos local...")
        local_conn = get_connection(LOCAL_DB_URL)
        print("OK - Conectado a local")
        
        # Limpiar datos locales
        clear_local_tables(local_conn)
        
        # Sincronizar en orden (respetando foreign keys)
        sync_operations = [
            ('colegios', ['id', 'nombre', 'comuna', 'created_at', 'updated_at']),
            ('equipos', ['id', 'nombre', 'descripcion', 'colegio_id', 'created_at', 'updated_at']),
            ('usuarios', ['id', 'email', 'hashed_password', 'nombre_completo', 'rol', 'equipo_id', 'is_active', 'created_at', 'updated_at']),
            ('tutores', ['id', 'nombre', 'apellido', 'email', 'equipo_id', 'created_at', 'updated_at']),
            ('estudiantes', ['id', 'rut', 'nombre', 'apellido', 'curso', 'equipo_id', 'nombre_apoderado', 'contacto_apoderado', 'observaciones', 'created_at', 'updated_at']),
            ('asistencia_tutores', ['id', 'tutor_id', 'semana', 'estado', 'created_at', 'updated_at']),
            ('asistencia_estudiantes', ['id', 'estudiante_id', 'semana', 'estado', 'created_at', 'updated_at'])
        ]
        
        for table_name, columns in sync_operations:
            sync_table(prod_conn, local_conn, table_name, columns)
        
        print("\nSINCRONIZACION COMPLETADA")
        print("Tu base de datos local ahora tiene los mismos datos que produccion")
        
    except Exception as e:
        print(f"ERROR durante la sincronizacion: {e}")
    finally:
        if prod_conn:
            prod_conn.close()
        if local_conn:
            local_conn.close()

if __name__ == "__main__":
    sync_database()
