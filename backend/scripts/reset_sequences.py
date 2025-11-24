"""
Script para resetear las secuencias de IDs en PostgreSQL
Esto corrige el error "Duplicate Key" cuando la secuencia está desincronizada
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

def reset_sequences():
    """Resetear las secuencias de IDs para asistencia_estudiantes y asistencia_tutores"""
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("[*] Reseteando secuencias de IDs...")
            
            # Resetear secuencia de asistencia_estudiantes
            print("\n[*] Reseteando asistencia_estudiantes...")
            result = conn.execute(text("""
                SELECT setval(
                    pg_get_serial_sequence('asistencia_estudiantes', 'id'),
                    COALESCE((SELECT MAX(id) FROM asistencia_estudiantes), 1),
                    true
                ) as new_value;
            """))
            new_value = result.scalar()
            print(f"   [OK] Secuencia reseteada. Nuevo valor: {new_value}")
            
            # Resetear secuencia de asistencia_tutores
            print("\n[*] Reseteando asistencia_tutores...")
            result = conn.execute(text("""
                SELECT setval(
                    pg_get_serial_sequence('asistencia_tutores', 'id'),
                    COALESCE((SELECT MAX(id) FROM asistencia_tutores), 1),
                    true
                ) as new_value;
            """))
            new_value = result.scalar()
            print(f"   [OK] Secuencia reseteada. Nuevo valor: {new_value}")
            
            # Verificar secuencias
            print("\n[*] Verificando secuencias...")
            result = conn.execute(text("""
                SELECT 
                    'asistencia_estudiantes' as tabla,
                    last_value as ultimo_valor,
                    (SELECT MAX(id) FROM asistencia_estudiantes) as max_id_tabla
                FROM asistencia_estudiantes_id_seq
                UNION ALL
                SELECT 
                    'asistencia_tutores' as tabla,
                    last_value as ultimo_valor,
                    (SELECT MAX(id) FROM asistencia_tutores) as max_id_tabla
                FROM asistencia_tutores_id_seq;
            """))
            
            print("\n[*] Estado de las secuencias:")
            for row in result:
                tabla = row[0]
                ultimo_valor = row[1]
                max_id_tabla = row[2]
                print(f"   {tabla}:")
                print(f"      Ultimo valor en secuencia: {ultimo_valor}")
                print(f"      Maximo ID en tabla: {max_id_tabla}")
                if ultimo_valor >= max_id_tabla:
                    print(f"      [OK] Secuencia correcta")
                else:
                    print(f"      [WARNING] Secuencia desincronizada")
            
            conn.commit()
            print("\n[OK] Secuencias reseteadas correctamente!")
            
    except Exception as e:
        print(f"\n[ERROR] Error al resetear secuencias: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    reset_sequences()

