# 🚀 Instrucciones para Configurar el Backend - Plataforma Tutorías

## 📋 Resumen de lo que hemos creado

Hemos creado una estructura completa del backend con:
- **FastAPI** como framework web
- **PostgreSQL** como base de datos
- **SQLAlchemy** como ORM
- **JWT** para autenticación
- **Alembic** para migraciones
- **Frontend** con login funcional

## 🗂️ Estructura del Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de FastAPI
│   ├── database.py             # Configuración de la base de datos
│   ├── models/                 # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── tutor.py
│   │   ├── student.py
│   │   └── school.py
│   ├── schemas/                # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── tutor.py
│   │   ├── student.py
│   │   └── school.py
│   ├── routers/                # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tutors.py
│   │   ├── students.py
│   │   └── schools.py
│   ├── auth/                   # Lógica de autenticación
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── dependencies.py
│   └── utils/                  # Utilidades
│       └── __init__.py
├── alembic/                    # Migraciones de base de datos
├── requirements.txt            # Dependencias Python
├── init_db.py                  # Script para inicializar BD
└── README.md                   # Documentación
```

## 🔧 PASOS PARA EJECUTAR

### 1. Crear el archivo .env

Crea un archivo `.env` en la carpeta `backend` con este contenido:

```env
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/tutorias_db
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ IMPORTANTE:** Reemplaza `TU_CONTRASEÑA` con la contraseña real de tu PostgreSQL.

### 2. Crear la base de datos

En tu terminal de PostgreSQL (donde ya estás conectado):

```sql
CREATE DATABASE tutorias_db;
\q
```

### 3. Instalar dependencias del backend

```bash
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Inicializar la base de datos

```bash
# Asegúrate de estar en la carpeta backend y con el entorno virtual activado
python init_db.py
```

Este comando creará las tablas y agregará datos de ejemplo.

### 5. Ejecutar el servidor backend

```bash
# Asegúrate de estar en la carpeta backend y con el entorno virtual activado
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: http://localhost:8000

### 6. Ejecutar el frontend

En una nueva terminal (mantén el backend corriendo):

```bash
# Navegar a la carpeta raíz del proyecto
cd ..

# Instalar dependencias del frontend (si no lo has hecho)
npm install

# Ejecutar el frontend
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## 🔑 Credenciales de Prueba

Después de ejecutar `init_db.py`, tendrás estos usuarios:

- **Administrador**: 
  - Email: `admin@tutorias.com`
  - Contraseña: `admin123`

- **Tutor**: 
  - Email: `tutor@tutorias.com`
  - Contraseña: `tutor123`

## 📚 Endpoints de la API

Una vez que el backend esté corriendo, puedes probar estos endpoints:

- **Documentación interactiva**: http://localhost:8000/docs
- **Login**: `POST http://localhost:8000/auth/login-json`
- **Obtener colegios**: `GET http://localhost:8000/schools/`
- **Obtener tutores**: `GET http://localhost:8000/tutors/`
- **Obtener estudiantes**: `GET http://localhost:8000/students/`

## 🧪 Probar el Login

1. Abre http://localhost:5173 en tu navegador
2. Verás la página de login
3. Usa las credenciales de prueba:
   - Email: `admin@tutorias.com`
   - Contraseña: `admin123`
4. Después del login exitoso, verás el dashboard con tu nombre y rol

## 🗄️ Verificar la Base de Datos

Puedes verificar que las tablas se crearon correctamente:

```sql
-- Conectarse a la base de datos
\c tutorias_db

-- Ver las tablas
\dt

-- Ver datos de usuarios
SELECT * FROM users;

-- Ver datos de colegios
SELECT * FROM schools;

-- Ver datos de tutores
SELECT * FROM tutors;

-- Ver datos de estudiantes
SELECT * FROM students;
```

## 🚨 Solución de Problemas

### Error de conexión a la base de datos
- Verifica que PostgreSQL esté corriendo
- Verifica que la contraseña en el archivo `.env` sea correcta
- Verifica que la base de datos `tutorias_db` exista

### Error de dependencias
- Asegúrate de estar en el entorno virtual: `venv\Scripts\activate`
- Reinstala las dependencias: `pip install -r requirements.txt`

### Error de CORS en el frontend
- Verifica que el backend esté corriendo en el puerto 8000
- Verifica que el frontend esté corriendo en el puerto 5173

## ✅ Verificación Final

Si todo funciona correctamente, deberías poder:

1. ✅ Ver la página de login en http://localhost:5173
2. ✅ Iniciar sesión con las credenciales de prueba
3. ✅ Ver el dashboard con tu información de usuario
4. ✅ Navegar entre las diferentes secciones
5. ✅ Cerrar sesión y volver a la página de login
6. ✅ Ver la documentación de la API en http://localhost:8000/docs

## 🎉 ¡Listo!

Ahora tienes un sistema completo de autenticación funcionando con:
- Backend FastAPI con PostgreSQL
- Frontend React con login
- Sistema de roles (admin/tutor)
- API REST completa
- Documentación automática

¡El siguiente paso sería agregar más funcionalidades a cada sección de la aplicación!
