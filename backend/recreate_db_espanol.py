"""
Script para recrear la base de datos con las nuevas tablas en español
"""
from sqlalchemy import text
from app.database import engine
from app import models

def recreate_db():
    """Recrea la base de datos eliminando todas las tablas y creando las nuevas"""
    try:
        # Conectar a la base de datos
        with engine.connect() as conn:
            # Eliminar todas las tablas existentes
            print("Eliminando tablas existentes...")
            
            # Obtener todas las tablas
            result = conn.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public' 
                AND tablename NOT LIKE 'alembic%'
            """))
            
            tables = [row[0] for row in result]
            
            # Eliminar cada tabla
            for table in tables:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    print(f"   - Tabla {table} eliminada")
                except Exception as e:
                    print(f"   - Error eliminando tabla {table}: {e}")
            
            # Confirmar los cambios
            conn.commit()
            print("Todas las tablas eliminadas correctamente.")
            
        # Crear las nuevas tablas
        print("Creando nuevas tablas en español...")
        models.Base.metadata.create_all(bind=engine)
        print("Nuevas tablas creadas correctamente.")
        
    except Exception as e:
        print(f"Error al recrear la base de datos: {e}")

if __name__ == "__main__":
    recreate_db()
