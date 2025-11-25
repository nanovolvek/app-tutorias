"""
Script para agregar campos de deserción a las tablas estudiantes y tutores
Ejecuta el SQL necesario para agregar los campos activo y motivo_desercion
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

def add_desercion_fields():
    """Agregar campos activo y motivo_desercion a estudiantes y tutores"""
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("[*] Agregando campos de deserción...")
            
            # Agregar campos a estudiantes
            print("\n[*] Agregando campos a tabla estudiantes...")
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE,
                ADD COLUMN IF NOT EXISTS motivo_desercion VARCHAR;
            """))
            print("   [OK] Campos agregados a estudiantes")
            
            # Agregar campos a tutores
            print("\n[*] Agregando campos a tabla tutores...")
            conn.execute(text("""
                ALTER TABLE tutores 
                ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE,
                ADD COLUMN IF NOT EXISTS motivo_desercion VARCHAR;
            """))
            print("   [OK] Campos agregados a tutores")
            
            # Verificar que los campos se agregaron correctamente
            print("\n[*] Verificando campos...")
            result = conn.execute(text("""
                SELECT 
                    'estudiantes' as tabla,
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_name = 'estudiantes' 
                AND column_name IN ('activo', 'motivo_desercion')
                UNION ALL
                SELECT 
                    'tutores' as tabla,
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_name = 'tutores' 
                AND column_name IN ('activo', 'motivo_desercion')
                ORDER BY tabla, column_name;
            """))
            
            print("\n[*] Campos en la base de datos:")
            for row in result:
                tabla = row[0]
                column_name = row[1]
                data_type = row[2]
                is_nullable = row[3]
                column_default = row[4]
                print(f"   {tabla}.{column_name}:")
                print(f"      Tipo: {data_type}")
                print(f"      Nullable: {is_nullable}")
                print(f"      Default: {column_default}")
            
            conn.commit()
            print("\n[OK] Campos agregados correctamente!")
            
    except Exception as e:
        print(f"\n[ERROR] Error al agregar campos: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    add_desercion_fields()

