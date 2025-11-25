-- Script para actualizar todos los registros existentes a activo = true
-- Ejecutar este script en la base de datos de producción

-- Actualizar todos los estudiantes a activo = true
UPDATE estudiantes 
SET activo = TRUE 
WHERE activo IS NULL OR activo = FALSE;

-- Actualizar todos los tutores a activo = true
UPDATE tutores 
SET activo = TRUE 
WHERE activo IS NULL OR activo = FALSE;

-- Verificar que todos los registros tienen activo = true
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

