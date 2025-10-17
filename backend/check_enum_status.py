#!/usr/bin/env python3
"""
Script para verificar el estado del enum
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def check_enum_status():
    """Verificar el estado del enum"""
    print("Verificando estado del enum...")
    
    # Configurar URL de producción
    prod_db_url = 'postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres'
    engine = create_engine(prod_db_url)
    
    try:
        with engine.connect() as conn:
            # Verificar el tipo de la columna estado
            print("Tipo de columna estado:")
            tipo_columna = conn.execute(text("""
                SELECT data_type, udt_name
                FROM information_schema.columns
                WHERE table_name = 'asistencia_estudiantes' AND column_name = 'estado'
            """)).fetchone()
            
            print(f"  Tipo: {tipo_columna[0]}, UDT: {tipo_columna[1]}")
            
            # Verificar valores del enum
            print("\nValores del enum:")
            try:
                enum_values = conn.execute(text("""
                    SELECT unnest(enum_range(NULL::estadoasistencia))
                """)).fetchall()
                
                for valor in enum_values:
                    print(f"  '{valor[0]}'")
            except Exception as e:
                print(f"  Error obteniendo valores del enum: {e}")
            
            # Verificar datos reales en la tabla
            print("\nDatos reales en asistencia_estudiantes:")
            estados_reales = conn.execute(text("""
                SELECT DISTINCT estado, COUNT(*) as cantidad
                FROM asistencia_estudiantes
                GROUP BY estado
                ORDER BY estado
            """)).fetchall()
            
            for estado in estados_reales:
                print(f"  '{estado[0]}': {estado[1]} registros")
            
            return True
            
    except Exception as e:
        print(f"Error verificando enum: {e}")
        return False

def main():
    """Función principal"""
    print("VERIFICANDO ESTADO DEL ENUM")
    print("=" * 40)
    
    success = check_enum_status()
    
    if success:
        print("\nVerificacion completada!")
    else:
        print("\nError en la verificacion")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
