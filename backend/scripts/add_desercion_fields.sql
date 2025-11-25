-- Script para agregar campos de deserción a las tablas estudiantes y tutores
-- Ejecutar este script en la base de datos de producción

-- Agregar campos a la tabla estudiantes
ALTER TABLE estudiantes 
ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS motivo_desercion VARCHAR;

-- Agregar campos a la tabla tutores
ALTER TABLE tutores 
ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS motivo_desercion VARCHAR;

-- Verificar que los campos se agregaron correctamente
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

