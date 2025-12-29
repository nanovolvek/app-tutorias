-- Script de migración para agregar campos de gestión de contraseñas
-- Ejecutar este script en la base de datos para agregar los nuevos campos

-- Agregar campo password_changed (si no existe)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'usuarios' AND column_name = 'password_changed'
    ) THEN
        ALTER TABLE usuarios ADD COLUMN password_changed BOOLEAN DEFAULT FALSE NOT NULL;
    END IF;
END $$;

-- Agregar campo password_reset_token (si no existe)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'usuarios' AND column_name = 'password_reset_token'
    ) THEN
        ALTER TABLE usuarios ADD COLUMN password_reset_token VARCHAR;
    END IF;
END $$;

-- Agregar campo password_reset_expires (si no existe)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'usuarios' AND column_name = 'password_reset_expires'
    ) THEN
        ALTER TABLE usuarios ADD COLUMN password_reset_expires TIMESTAMP WITH TIME ZONE;
    END IF;
END $$;

-- Actualizar usuarios existentes para que tengan password_changed = true
-- (asumiendo que los usuarios existentes ya cambiaron su contraseña)
UPDATE usuarios SET password_changed = TRUE WHERE password_changed IS NULL OR password_changed = FALSE;

-- Verificar que los campos se agregaron correctamente
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'usuarios' 
AND column_name IN ('password_changed', 'password_reset_token', 'password_reset_expires')
ORDER BY column_name;

