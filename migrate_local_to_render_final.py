import pandas as pd
from sqlalchemy import create_engine, text
import os

# URL de la base de datos local (ajusta según tu configuración)
LOCAL_DATABASE_URL = os.getenv("LOCAL_DATABASE_URL", "postgresql://postgres:nanopostgres@localhost:5432/tutorias_db")
RENDER_DATABASE_URL = "postgresql://tutorias_db_user:kDL6FlvxRo9urc0X7DHUi86RHi0F2ec2@dpg-d3pr88c9c44c73c9snsg-a.oregon-postgres.render.com/tutorias_db"

def migrate_data():
    """Migra datos desde base de datos local a Render PostgreSQL"""
    
    print("Iniciando migracion desde base de datos local a Render...")
    
    try:
        # Conectar a base de datos local
        print("Conectando a base de datos local...")
        local_engine = create_engine(LOCAL_DATABASE_URL)
        
        # Conectar a Render PostgreSQL
        print("Conectando a Render PostgreSQL...")
        render_engine = create_engine(RENDER_DATABASE_URL)
        
        # Lista de tablas a migrar (en orden correcto de dependencias)
        tables = [
            'colegios',    # Sin dependencias
            'equipos',     # Sin dependencias
            'usuarios',    # Depende de equipos
            'tutores',     # Depende de equipos
            'estudiantes', # Depende de equipos
            'asistencias'  # Depende de estudiantes
        ]
        
        for table in tables:
            print(f"Migrando tabla: {table}")
            
            try:
                # Leer datos de base de datos local
                with local_engine.connect() as local_conn:
                    # Verificar si la tabla existe
                    check_table = text(f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = '{table}'
                        );
                    """)
                    table_exists = local_conn.execute(check_table).scalar()
                    
                    if table_exists:
                        query = f"SELECT * FROM {table}"
                        df = pd.read_sql(query, local_conn)
                        
                        if not df.empty:
                            print(f"   Encontrados {len(df)} registros en {table}")
                            
                            # Escribir datos a Render PostgreSQL
                            with render_engine.connect() as render_conn:
                                # Usar to_sql con if_exists='append' para agregar datos
                                df.to_sql(table, render_conn, if_exists='append', index=False, method='multi')
                                print(f"   Migrados {len(df)} registros a Render")
                        else:
                            print(f"   Tabla {table} esta vacia")
                    else:
                        print(f"   Tabla {table} no existe en la base de datos local")
                        
            except Exception as e:
                print(f"   Error migrando tabla {table}: {e}")
                continue
        
        print("Migracion completada exitosamente!")
        print("Ahora puedes usar las credenciales:")
        print("   admin@tutorias.com / admin123")
        print("   tutor1@tutorias.com / tutor123")
        print("   tutor2@tutorias.com / tutor123")
        
    except Exception as e:
        print(f"Error durante la migracion: {e}")
        return False
    
    finally:
        # Cerrar conexiones
        if 'local_engine' in locals():
            local_engine.dispose()
        if 'render_engine' in locals():
            render_engine.dispose()

if __name__ == "__main__":
    migrate_data()
