-- Script para verificar la conexión a la base de datos y las columnas
-- Ejecutar este script en DBeaver para verificar

-- Verificar que estás en la base de datos correcta
SELECT current_database();

-- Verificar columnas en estudiantes
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'estudiantes' 
AND column_name IN ('activo', 'motivo_desercion')
ORDER BY column_name;

-- Verificar columnas en tutores
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'tutores' 
AND column_name IN ('activo', 'motivo_desercion')
ORDER BY column_name;

-- Ver todas las columnas de estudiantes
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'estudiantes'
ORDER BY ordinal_position;

-- Ver todas las columnas de tutores
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'tutores'
ORDER BY ordinal_position;

