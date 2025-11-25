"""
Script para FORZAR la creación de columnas (sin IF NOT EXISTS)
Esto asegura que las columnas se agreguen incluso si hay problemas de caché
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos de producción
# FORZAR la URL de producción (no usar .env local)
DATABASE_URL = "postgresql://tutorias_db_user:kDL6FlvxRo9urc0X7DHUi86RHi0F2ec2@dpg-d3pr88c9c44c73c9snsg-a.oregon-postgres.render.com:5432/tutorias_db"
print(f"[*] Usando URL de producción (hardcoded)")

def force_add_columns():
    """Forzar la creación de columnas"""
    try:
        print(f"[*] Conectando a: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'base de datos'}")
        engine = create_engine(DATABASE_URL)
        
        with engine.begin() as conn:  # Usar begin() para transacción automática
            print("[*] Verificando columnas existentes...")
            
            # Verificar si las columnas ya existen
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'estudiantes' 
                AND column_name IN ('activo', 'motivo_desercion')
            """))
            existing_estudiantes = [row[0] for row in result]
            
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'tutores' 
                AND column_name IN ('activo', 'motivo_desercion')
            """))
            existing_tutores = [row[0] for row in result]
            
            print(f"   Columnas existentes en estudiantes: {existing_estudiantes}")
            print(f"   Columnas existentes en tutores: {existing_tutores}")
            
            # Agregar columnas a estudiantes si no existen
            if 'activo' not in existing_estudiantes:
                print("\n[*] Agregando columna 'activo' a estudiantes...")
                conn.execute(text("ALTER TABLE estudiantes ADD COLUMN activo BOOLEAN DEFAULT TRUE"))
                print("   [OK] Columna 'activo' agregada")
            else:
                print("\n[*] Columna 'activo' ya existe en estudiantes")
            
            if 'motivo_desercion' not in existing_estudiantes:
                print("\n[*] Agregando columna 'motivo_desercion' a estudiantes...")
                conn.execute(text("ALTER TABLE estudiantes ADD COLUMN motivo_desercion VARCHAR"))
                print("   [OK] Columna 'motivo_desercion' agregada")
            else:
                print("\n[*] Columna 'motivo_desercion' ya existe en estudiantes")
            
            # Agregar columnas a tutores si no existen
            if 'activo' not in existing_tutores:
                print("\n[*] Agregando columna 'activo' a tutores...")
                conn.execute(text("ALTER TABLE tutores ADD COLUMN activo BOOLEAN DEFAULT TRUE"))
                print("   [OK] Columna 'activo' agregada")
            else:
                print("\n[*] Columna 'activo' ya existe en tutores")
            
            if 'motivo_desercion' not in existing_tutores:
                print("\n[*] Agregando columna 'motivo_desercion' a tutores...")
                conn.execute(text("ALTER TABLE tutores ADD COLUMN motivo_desercion VARCHAR"))
                print("   [OK] Columna 'motivo_desercion' agregada")
            else:
                print("\n[*] Columna 'motivo_desercion' ya existe en tutores")
            
            # Actualizar valores NULL a TRUE
            print("\n[*] Actualizando valores NULL a TRUE...")
            conn.execute(text("UPDATE estudiantes SET activo = TRUE WHERE activo IS NULL"))
            conn.execute(text("UPDATE tutores SET activo = TRUE WHERE activo IS NULL"))
            
            # Verificar final
            print("\n[*] Verificación final de columnas...")
            result = conn.execute(text("""
                SELECT 
                    'estudiantes' as tabla,
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_name = 'estudiantes' 
                AND column_name IN ('activo', 'motivo_desercion')
                UNION ALL
                SELECT 
                    'tutores' as tabla,
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_name = 'tutores' 
                AND column_name IN ('activo', 'motivo_desercion')
                ORDER BY tabla, column_name;
            """))
            
            print("\n[*] Columnas finales en la base de datos:")
            for row in result:
                tabla = row[0]
                column_name = row[1]
                data_type = row[2]
                is_nullable = row[3]
                print(f"   {tabla}.{column_name}: {data_type} (nullable: {is_nullable})")
            
            print("\n[OK] Proceso completado!")
            
    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    force_add_columns()

