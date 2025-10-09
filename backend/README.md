# Plataforma Tutorías - Backend

Backend de la aplicación de gestión de tutorías desarrollado con FastAPI y PostgreSQL.

## 🚀 Instalación y Configuración

### 1. Crear entorno virtual

```bash
# Desde la carpeta backend
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la carpeta `backend` con el siguiente contenido:

```env
DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/tutorias_db
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Importante:** Reemplaza `tu_contraseña` con la contraseña real de tu base de datos PostgreSQL.

### 4. Crear la base de datos

```sql
-- Conectarse a PostgreSQL y ejecutar:
CREATE DATABASE tutorias_db;
```

### 5. Inicializar la base de datos

```bash
python init_db.py
```

Este script creará las tablas y agregará datos de ejemplo.

### 6. Ejecutar el servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: http://localhost:8000

## 📚 Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Credenciales de Prueba

Después de ejecutar `init_db.py`, tendrás estos usuarios disponibles:

- **Administrador**: 
  - Email: `admin@tutorias.com`
  - Contraseña: `admin123`

- **Tutor**: 
  - Email: `tutor@tutorias.com`
  - Contraseña: `tutor123`

## 🗄️ Estructura de la Base de Datos

### Tablas principales:

1. **users**: Usuarios del sistema (admin/tutor)
2. **schools**: Colegios donde se realizan las tutorías
3. **tutors**: Tutores voluntarios
4. **students**: Estudiantes que reciben tutorías

## 🔧 Endpoints Principales

- `POST /auth/login` - Iniciar sesión
- `GET /schools/` - Listar colegios
- `POST /schools/` - Crear colegio (solo admin)
- `GET /tutors/` - Listar tutores
- `POST /tutors/` - Crear tutor (solo admin)
- `GET /students/` - Listar estudiantes
- `POST /students/` - Crear estudiante (solo admin)

## 🛠️ Comandos Útiles

```bash
# Crear migración con Alembic
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Ver historial de migraciones
alembic history

# Revertir migración
alembic downgrade -1
```
