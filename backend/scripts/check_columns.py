"""
Script para verificar si las columnas activo y motivo_desercion existen en las tablas
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos de producción
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://tutorias_db_user:kDL6FlvxRo9urc0X7DHUi86RHi0F2ec2@dpg-d3pr88c9c44c73c9snsg-a.oregon-postgres.render.com:5432/tutorias_db"
)

def check_columns():
    """Verificar si las columnas existen"""
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("[*] Verificando columnas en la base de datos...")
            
            # Verificar columnas en estudiantes
            print("\n[*] Verificando tabla estudiantes...")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'estudiantes' 
                AND column_name IN ('activo', 'motivo_desercion')
                ORDER BY column_name;
            """))
            
            estudiantes_cols = list(result)
            if estudiantes_cols:
                print("   [OK] Columnas encontradas en estudiantes:")
                for row in estudiantes_cols:
                    print(f"      - {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")
            else:
                print("   [ERROR] No se encontraron las columnas activo o motivo_desercion en estudiantes")
            
            # Verificar columnas en tutores
            print("\n[*] Verificando tabla tutores...")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'tutores' 
                AND column_name IN ('activo', 'motivo_desercion')
                ORDER BY column_name;
            """))
            
            tutores_cols = list(result)
            if tutores_cols:
                print("   [OK] Columnas encontradas en tutores:")
                for row in tutores_cols:
                    print(f"      - {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")
            else:
                print("   [ERROR] No se encontraron las columnas activo o motivo_desercion en tutores")
            
            # Listar todas las columnas para ver qué hay
            print("\n[*] Todas las columnas en estudiantes:")
            result = conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'estudiantes'
                ORDER BY ordinal_position;
            """))
            for row in result:
                print(f"      - {row[0]}: {row[1]}")
            
            print("\n[*] Todas las columnas en tutores:")
            result = conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'tutores'
                ORDER BY ordinal_position;
            """))
            for row in result:
                print(f"      - {row[0]}: {row[1]}")
            
    except Exception as e:
        print(f"\n[ERROR] Error al verificar columnas: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    check_columns()

