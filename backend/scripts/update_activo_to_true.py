"""
Script para actualizar todos los registros existentes a activo = true
Marca todos los estudiantes y tutores como activos
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

def update_activo_to_true():
    """Actualizar todos los registros a activo = true"""
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("[*] Actualizando registros a activo = true...")
            
            # Actualizar estudiantes
            print("\n[*] Actualizando estudiantes...")
            result = conn.execute(text("""
                UPDATE estudiantes 
                SET activo = TRUE 
                WHERE activo IS NULL OR activo = FALSE;
            """))
            estudiantes_actualizados = result.rowcount
            print(f"   [OK] {estudiantes_actualizados} estudiantes actualizados")
            
            # Actualizar tutores
            print("\n[*] Actualizando tutores...")
            result = conn.execute(text("""
                UPDATE tutores 
                SET activo = TRUE 
                WHERE activo IS NULL OR activo = FALSE;
            """))
            tutores_actualizados = result.rowcount
            print(f"   [OK] {tutores_actualizados} tutores actualizados")
            
            # Verificar estado
            print("\n[*] Verificando estado de los registros...")
            result = conn.execute(text("""
                SELECT 
                    'estudiantes' as tabla,
                    COUNT(*) as total,
                    COUNT(CASE WHEN activo = TRUE THEN 1 END) as activos,
                    COUNT(CASE WHEN activo = FALSE THEN 1 END) as inactivos,
                    COUNT(CASE WHEN activo IS NULL THEN 1 END) as nulos
                FROM estudiantes
                UNION ALL
                SELECT 
                    'tutores' as tabla,
                    COUNT(*) as total,
                    COUNT(CASE WHEN activo = TRUE THEN 1 END) as activos,
                    COUNT(CASE WHEN activo = FALSE THEN 1 END) as inactivos,
                    COUNT(CASE WHEN activo IS NULL THEN 1 END) as nulos
                FROM tutores;
            """))
            
            print("\n[*] Estado de los registros:")
            for row in result:
                tabla = row[0]
                total = row[1]
                activos = row[2]
                inactivos = row[3]
                nulos = row[4]
                print(f"   {tabla}:")
                print(f"      Total: {total}")
                print(f"      Activos: {activos}")
                print(f"      Inactivos: {inactivos}")
                print(f"      Nulos: {nulos}")
            
            conn.commit()
            print("\n[OK] Registros actualizados correctamente!")
            
    except Exception as e:
        print(f"\n[ERROR] Error al actualizar registros: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    update_activo_to_true()

