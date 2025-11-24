-- Script para resetear las secuencias de IDs en PostgreSQL
-- Esto corrige el error "Duplicate Key" cuando la secuencia está desincronizada
-- Ejecutar este script en la base de datos de producción

-- Resetear secuencia de asistencia_estudiantes
SELECT setval(
    pg_get_serial_sequence('asistencia_estudiantes', 'id'),
    COALESCE((SELECT MAX(id) FROM asistencia_estudiantes), 1),
    true
);

-- Resetear secuencia de asistencia_tutores
SELECT setval(
    pg_get_serial_sequence('asistencia_tutores', 'id'),
    COALESCE((SELECT MAX(id) FROM asistencia_tutores), 1),
    true
);

-- Verificar que las secuencias están correctas
SELECT 
    'asistencia_estudiantes' as tabla,
    pg_get_serial_sequence('asistencia_estudiantes', 'id') as secuencia,
    last_value as ultimo_valor
FROM asistencia_estudiantes_id_seq
UNION ALL
SELECT 
    'asistencia_tutores' as tabla,
    pg_get_serial_sequence('asistencia_tutores', 'id') as secuencia,
    last_value as ultimo_valor
FROM asistencia_tutores_id_seq;

