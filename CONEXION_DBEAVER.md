# 🗄️ Guía para Conectarse a PostgreSQL desde DBeaver

## 📋 Información de la Base de Datos

- **Tipo de Base de Datos:** PostgreSQL
- **Host:** localhost
- **Puerto:** 5432
- **Nombre de la Base de Datos:** tutorias_db
- **Usuario:** postgres
- **Contraseña:** nanopostgres

## 🔧 Pasos para Conectarse desde DBeaver

### 1. Abrir DBeaver
- Inicia DBeaver en tu computadora

### 2. Crear Nueva Conexión
1. **Clic en el botón "Nueva Conexión"** (icono de enchufe con +)
2. **Seleccionar PostgreSQL** de la lista de bases de datos
3. **Clic en "Siguiente"**

### 3. Configurar Parámetros de Conexión

En la ventana de configuración, llenar los siguientes campos:

```
Host: localhost
Puerto: 5432
Base de datos: tutorias_db
Usuario: postgres
Contraseña: nanopostgres
```

### 4. Configuraciones Adicionales

1. **Pestaña "Principal":**
   - Host: `localhost`
   - Puerto: `5432`
   - Base de datos: `tutorias_db`
   - Usuario: `postgres`
   - Contraseña: `nanopostgres`

2. **Pestaña "Driver":**
   - Driver: PostgreSQL (debería estar seleccionado automáticamente)
   - Versión: PostgreSQL 12+ (o la que tengas instalada)

3. **Pestaña "Conexión":**
   - Timeout de conexión: `30` segundos
   - Timeout de lectura: `30` segundos

### 5. Probar la Conexión

1. **Clic en "Probar Conexión"**
2. **Verificar que aparezca "Conectado"** en verde
3. Si hay errores, verificar que PostgreSQL esté ejecutándose

### 6. Guardar y Conectar

1. **Clic en "Finalizar"**
2. **Asignar un nombre** a la conexión (ej: "Tutorias DB")
3. **Clic en "Aceptar"**
4. **Expandir la conexión** en el panel izquierdo

## 📊 Explorar la Base de Datos

### Ver las Tablas
1. **Expandir "tutorias_db"**
2. **Expandir "Esquemas"**
3. **Expandir "public"**
4. **Expandir "Tablas"**

### Tablas Disponibles
- **users** - Usuarios del sistema
- **schools** - Colegios
- **tutors** - Tutores
- **students** - Estudiantes

### Ver Datos de una Tabla
1. **Clic derecho en una tabla**
2. **Seleccionar "Ver datos"**
3. **Los datos se mostrarán en una nueva pestaña**

## 🔍 Consultas Útiles

### Ver todos los estudiantes con su colegio:
```sql
SELECT 
    s.id,
    s.first_name,
    s.last_name,
    s.course,
    sc.name as school_name,
    sc.comuna
FROM students s
JOIN schools sc ON s.school_id = sc.id
ORDER BY s.id;
```

### Ver todos los usuarios:
```sql
SELECT 
    id,
    email,
    full_name,
    role,
    is_active,
    created_at
FROM users
ORDER BY id;
```

### Ver todos los tutores con su colegio:
```sql
SELECT 
    t.id,
    t.first_name,
    t.last_name,
    t.email,
    sc.name as school_name,
    sc.comuna
FROM tutors t
JOIN schools sc ON t.school_id = sc.id
ORDER BY t.id;
```

### Ver todos los colegios:
```sql
SELECT 
    id,
    name,
    comuna,
    created_at
FROM schools
ORDER BY id;
```

## 🚨 Solución de Problemas

### Error: "Connection refused"
- **Verificar que PostgreSQL esté ejecutándose**
- **Verificar que el puerto 5432 esté disponible**

### Error: "Authentication failed"
- **Verificar usuario y contraseña**
- **Verificar que el usuario postgres tenga permisos**

### Error: "Database does not exist"
- **Verificar que la base de datos `tutorias_db` exista**
- **Crear la base de datos si no existe:**
  ```sql
  CREATE DATABASE tutorias_db;
  ```

### Error: "Driver not found"
- **DBeaver debería descargar automáticamente el driver de PostgreSQL**
- **Si no lo hace, descargar manualmente desde la configuración del driver**

## 📝 Comandos SQL Útiles

### Crear una nueva tabla:
```sql
CREATE TABLE mi_tabla (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);
```

### Insertar datos:
```sql
INSERT INTO schools (name, comuna) 
VALUES ('Nuevo Colegio', 'Providencia');
```

### Actualizar datos:
```sql
UPDATE students 
SET course = '4° Básico' 
WHERE id = 1;
```

### Eliminar datos:
```sql
DELETE FROM students 
WHERE id = 1;
```

## ✅ Verificación de Conexión Exitosa

Si la conexión es exitosa, deberías poder:
1. ✅ Ver la base de datos `tutorias_db` en el panel izquierdo
2. ✅ Expandir "Esquemas" → "public" → "Tablas"
3. ✅ Ver las 4 tablas: users, schools, tutors, students
4. ✅ Hacer clic derecho en cualquier tabla y seleccionar "Ver datos"
5. ✅ Ejecutar consultas SQL en el editor

## 🎉 ¡Listo!

Ahora puedes explorar y administrar tu base de datos de tutorías desde DBeaver de manera visual y fácil.

### Próximos Pasos:
- Explorar las tablas existentes
- Ejecutar consultas SQL personalizadas
- Exportar datos si es necesario
- Hacer respaldos de la base de datos
