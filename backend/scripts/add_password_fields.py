"""
Script para agregar campos de gestión de contraseñas a la tabla usuarios.
Ejecuta este script para actualizar la base de datos con los nuevos campos.
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_database_url():
    """Obtiene la URL de la base de datos desde variables de entorno"""
    # Primero intenta desde DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    
    # Si no existe, intenta construir desde variables individuales
    if not database_url:
        db_user = os.getenv("DB_USER", "tutorias_db_user")
        db_password = os.getenv("DB_PASSWORD", "kDL6FlvxRo9urc0X7DHUi86RHi0F2ec2")
        db_host = os.getenv("DB_HOST", "dpg-d3pr88c9c44c73c9snsg-a.oregon-postgres.render.com")
        db_name = os.getenv("DB_NAME", "tutorias_db")
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    
    return database_url

def check_column_exists(engine, table_name, column_name):
    """Verifica si una columna existe en una tabla"""
    query = text("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = :table_name AND column_name = :column_name
        )
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name, "column_name": column_name})
        return result.scalar()

def add_password_fields():
    """Agrega los campos de gestión de contraseñas a la tabla usuarios"""
    
    database_url = get_database_url()
    
    print("[*] Conectando a la base de datos...")
    print(f"    URL: {database_url.split('@')[0]}@***")  # Ocultar contraseña en el log
    
    try:
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        print("[OK] Conexion exitosa\n")
        
        # Verificar y agregar password_changed
        if not check_column_exists(engine, "usuarios", "password_changed"):
            print("[+] Agregando campo 'password_changed'...")
            with engine.connect() as conn:
                conn.execute(text("""
                    ALTER TABLE usuarios 
                    ADD COLUMN password_changed BOOLEAN DEFAULT FALSE NOT NULL
                """))
                conn.commit()
            print("    [OK] Campo 'password_changed' agregado")
        else:
            print("    [-] Campo 'password_changed' ya existe")
        
        # Verificar y agregar password_reset_token
        if not check_column_exists(engine, "usuarios", "password_reset_token"):
            print("[+] Agregando campo 'password_reset_token'...")
            with engine.connect() as conn:
                conn.execute(text("""
                    ALTER TABLE usuarios 
                    ADD COLUMN password_reset_token VARCHAR
                """))
                conn.commit()
            print("    [OK] Campo 'password_reset_token' agregado")
        else:
            print("    [-] Campo 'password_reset_token' ya existe")
        
        # Verificar y agregar password_reset_expires
        if not check_column_exists(engine, "usuarios", "password_reset_expires"):
            print("[+] Agregando campo 'password_reset_expires'...")
            with engine.connect() as conn:
                conn.execute(text("""
                    ALTER TABLE usuarios 
                    ADD COLUMN password_reset_expires TIMESTAMP WITH TIME ZONE
                """))
                conn.commit()
            print("    [OK] Campo 'password_reset_expires' agregado")
        else:
            print("    [-] Campo 'password_reset_expires' ya existe")
        
        # Actualizar usuarios existentes
        print("\n[*] Actualizando usuarios existentes...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                UPDATE usuarios 
                SET password_changed = TRUE 
                WHERE password_changed IS NULL OR password_changed = FALSE
            """))
            conn.commit()
            updated = result.rowcount
        print(f"    [OK] {updated} usuario(s) actualizado(s)")
        
        # Verificar campos agregados
        print("\n[*] Verificando campos agregados...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable, 
                    column_default
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' 
                AND column_name IN ('password_changed', 'password_reset_token', 'password_reset_expires')
                ORDER BY column_name
            """))
            
            columns = result.fetchall()
            if columns:
                print("\n    Campos encontrados:")
                for col in columns:
                    print(f"    - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
            else:
                print("    [ADVERTENCIA] No se encontraron los campos esperados")
        
        print("\n[OK] Migracion completada exitosamente!")
        print("\n[NOTA] Los usuarios existentes tienen password_changed = TRUE")
        print("       Los nuevos usuarios deberan cambiar su contraseña al primer login.")
        
    except Exception as e:
        print(f"\n[ERROR] Error durante la migracion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("  Migración: Agregar campos de gestión de contraseñas")
    print("=" * 60)
    print()
    
    add_password_fields()
    
    print("\n" + "=" * 60)

