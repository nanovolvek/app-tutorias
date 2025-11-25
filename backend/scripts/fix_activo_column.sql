-- Script para hacer la columna activo nullable temporalmente y luego actualizar todos los registros
-- Esto corrige problemas de compatibilidad

-- Hacer la columna activo nullable en estudiantes
ALTER TABLE estudiantes 
ALTER COLUMN activo DROP NOT NULL;

-- Hacer la columna activo nullable en tutores
ALTER TABLE tutores 
ALTER COLUMN activo DROP NOT NULL;

-- Actualizar todos los registros a activo = true
UPDATE estudiantes 
SET activo = TRUE 
WHERE activo IS NULL;

UPDATE tutores 
SET activo = TRUE 
WHERE activo IS NULL;

-- Verificar estado
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

