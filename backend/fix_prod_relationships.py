#!/usr/bin/env python3
"""
Script para corregir las relaciones en la base de datos de producción
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def fix_relationships():
    """Corregir las relaciones entre equipos, colegios, estudiantes y tutores"""
    print("Corrigiendo relaciones en la base de datos de produccion...")
    
    # Configurar URL de producción
    prod_db_url = 'postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres'
    engine = create_engine(prod_db_url)
    
    try:
        with engine.connect() as conn:
            # 1. Verificar que existan los equipos y colegios
            print("Verificando equipos...")
            equipos = conn.execute(text("SELECT id, nombre FROM equipos ORDER BY id")).fetchall()
            print(f"Equipos encontrados: {len(equipos)}")
            for equipo in equipos:
                print(f"  - {equipo[0]}: {equipo[1]}")
            
            print("\nVerificando colegios...")
            colegios = conn.execute(text("SELECT id, nombre FROM colegios ORDER BY id")).fetchall()
            print(f"Colegios encontrados: {len(colegios)}")
            for colegio in colegios:
                print(f"  - {colegio[0]}: {colegio[1]}")
            
            # 2. Asignar colegios a equipos
            print("\nAsignando colegios a equipos...")
            conn.execute(text("""
                UPDATE equipos 
                SET colegio_id = 1 
                WHERE id = 1
            """))  # Equipo A -> Colegio San Patricio
            
            conn.execute(text("""
                UPDATE equipos 
                SET colegio_id = 2 
                WHERE id = 2
            """))  # Equipo B -> Liceo Manuel Barros Borgoño
            
            conn.execute(text("""
                UPDATE equipos 
                SET colegio_id = 3 
                WHERE id = 3
            """))  # Equipo C -> Instituto Nacional
            
            # 3. Asignar equipos a estudiantes
            print("Asignando equipos a estudiantes...")
            # Equipo A (estudiantes 1-5)
            conn.execute(text("""
                UPDATE estudiantes 
                SET equipo_id = 1 
                WHERE id IN (1, 2, 3, 4, 5)
            """))
            
            # Equipo B (estudiantes 6-10)
            conn.execute(text("""
                UPDATE estudiantes 
                SET equipo_id = 2 
                WHERE id IN (6, 7, 8, 9, 10)
            """))
            
            # Equipo C (estudiantes 11-15)
            conn.execute(text("""
                UPDATE estudiantes 
                SET equipo_id = 3 
                WHERE id IN (11, 12, 13, 14, 15)
            """))
            
            # 4. Asignar equipos a tutores
            print("Asignando equipos a tutores...")
            # Tutores 1-2 -> Equipo A
            conn.execute(text("""
                UPDATE tutores 
                SET equipo_id = 1 
                WHERE id IN (1, 2)
            """))
            
            # Tutores 3-4 -> Equipo B
            conn.execute(text("""
                UPDATE tutores 
                SET equipo_id = 2 
                WHERE id IN (3, 4)
            """))
            
            # Tutores 5-6 -> Equipo C
            conn.execute(text("""
                UPDATE tutores 
                SET equipo_id = 3 
                WHERE id IN (5, 6)
            """))
            
            # 5. Verificar las relaciones
            print("\nVerificando relaciones corregidas...")
            
            # Verificar estudiantes con equipos
            estudiantes_con_equipos = conn.execute(text("""
                SELECT e.nombre, e.apellido, eq.nombre as equipo, c.nombre as colegio
                FROM estudiantes e
                LEFT JOIN equipos eq ON e.equipo_id = eq.id
                LEFT JOIN colegios c ON eq.colegio_id = c.id
                ORDER BY e.id
            """)).fetchall()
            
            print("Estudiantes con equipos y colegios:")
            for est in estudiantes_con_equipos:
                print(f"  - {est[0]} {est[1]} -> {est[2]} -> {est[3]}")
            
            # Verificar tutores con equipos
            tutores_con_equipos = conn.execute(text("""
                SELECT t.nombre, t.apellido, eq.nombre as equipo, c.nombre as colegio
                FROM tutores t
                LEFT JOIN equipos eq ON t.equipo_id = eq.id
                LEFT JOIN colegios c ON eq.colegio_id = c.id
                ORDER BY t.id
            """)).fetchall()
            
            print("\nTutores con equipos y colegios:")
            for tut in tutores_con_equipos:
                print(f"  - {tut[0]} {tut[1]} -> {tut[2]} -> {tut[3]}")
            
            conn.commit()
            print("\nRelaciones corregidas exitosamente!")
            return True
            
    except Exception as e:
        print(f"Error corrigiendo relaciones: {e}")
        return False

def main():
    """Función principal"""
    print("INICIANDO CORRECCION DE RELACIONES EN PRODUCCION")
    print("=" * 60)
    
    success = fix_relationships()
    
    if success:
        print("\n" + "=" * 60)
        print("CORRECCION COMPLETADA EXITOSAMENTE!")
        print("Ahora la aplicacion en produccion deberia mostrar:")
        print("- Equipos y colegios correctamente asignados")
        print("- Datos de asistencia funcionando")
        print("- Graficos y estadisticas visibles")
    else:
        print("\nError en la correccion de relaciones")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
