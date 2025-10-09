# 🚀 Guía Completa para Ejecutar la Aplicación de Tutorías

## 📋 Resumen de la Aplicación

Esta es una aplicación web completa de gestión de tutorías con:
- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI + PostgreSQL
- **Autenticación:** JWT con roles (admin/tutor)
- **Base de datos:** PostgreSQL con datos de ejemplo

## 🗂️ Estructura del Proyecto

```
app-tutorias/
├── src/                          # Frontend React
│   ├── components/               # Componentes reutilizables
│   ├── pages/                    # Páginas de la aplicación
│   ├── contexts/                 # Contextos de React (Auth)
│   └── ...
├── backend/                      # Backend FastAPI
│   ├── app/                      # Código de la aplicación
│   ├── venv/                     # Entorno virtual Python
│   └── .env                      # Variables de entorno
└── ...
```

## 🔧 PASOS PARA EJECUTAR LA APLICACIÓN

### 1. Prerrequisitos

Asegúrate de tener instalado:
- **Node.js** (versión 16 o superior)
- **Python** (versión 3.8 o superior)
- **PostgreSQL** (con usuario `postgres` y contraseña `nanopostgres`)

### 2. Configurar la Base de Datos

1. **Conectarse a PostgreSQL:**
   ```bash
   psql -U postgres
   ```

2. **Crear la base de datos:**
   ```sql
   CREATE DATABASE tutorias_db;
   \q
   ```

### 3. Configurar el Backend

1. **Navegar al directorio backend:**
   ```bash
   cd backend
   ```

2. **Activar el entorno virtual:**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias (si es necesario):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar archivo .env:**
   El archivo `backend/.env` debe contener:
   ```
   DATABASE_URL=postgresql://postgres:nanopostgres@localhost:5432/tutorias_db
   SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_123456789_para_jwt_tokens
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Inicializar la base de datos:**
   ```bash
   python init_db.py
   ```

6. **Ejecutar el backend:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   El backend estará disponible en: http://localhost:8000

### 4. Configurar el Frontend

1. **Abrir una nueva terminal** (mantener el backend corriendo)

2. **Navegar al directorio raíz:**
   ```bash
   cd ..  # Si estás en la carpeta backend
   ```

3. **Instalar dependencias:**
   ```bash
   npm install
   ```

4. **Ejecutar el frontend:**
   ```bash
   npm run dev
   ```

   El frontend estará disponible en: http://localhost:5173

## 🔑 Credenciales de Prueba

- **Administrador:**
  - Email: `admin@tutorias.com`
  - Contraseña: `admin`

- **Tutor:**
  - Email: `tutor@tutorias.com`
  - Contraseña: `tutor`

## 🎯 Cómo Usar la Aplicación

1. **Abrir el navegador** y ir a: http://localhost:5173
2. **Iniciar sesión** con las credenciales de prueba
3. **Navegar** por el menú lateral para acceder a las diferentes secciones:
   - 📊 Dashboard
   - 👥 Estudiantes
   - 👨‍🏫 Tutores
   - ✅ Asistencia
   - 📝 Pruebas
   - 🎫 Tickets
   - 📚 Material de Apoyo

## 🔍 Verificar que Todo Funciona

### Backend:
- **Health check:** http://localhost:8000/health
- **Documentación API:** http://localhost:8000/docs

### Frontend:
- **Aplicación:** http://localhost:5173
- **Login funcional** con las credenciales de prueba

## 🚨 Solución de Problemas

### Error: "uvicorn no se reconoce"
```bash
# Usar python -m uvicorn en lugar de uvicorn directamente
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Error: "Cannot find package '@vitejs/plugin-react'"
```bash
# Instalar el plugin faltante
npm install @vitejs/plugin-react --save-dev
```

### Error de conexión a la base de datos
- Verificar que PostgreSQL esté corriendo
- Verificar la contraseña en el archivo `.env`
- Verificar que la base de datos `tutorias_db` exista

### Error de CORS
- Verificar que el backend esté corriendo en puerto 8000
- Verificar que el frontend esté corriendo en puerto 5173

## 📝 Comandos Rápidos

### Iniciar todo desde cero:
```bash
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd ..
npm run dev
```

### Verificar puertos:
```bash
# Windows
netstat -an | findstr ":8000\|:5173"

# Linux/Mac
netstat -an | grep ":8000\|:5173"
```

## ✅ Verificación Final

Si todo funciona correctamente, deberías poder:
1. ✅ Ver la página de login en http://localhost:5173
2. ✅ Iniciar sesión con las credenciales de prueba
3. ✅ Ver el dashboard con tu información de usuario
4. ✅ Navegar entre las diferentes secciones
5. ✅ Cerrar sesión y volver a la página de login
6. ✅ Ver la documentación de la API en http://localhost:8000/docs

## 🎉 ¡Listo!

Tu aplicación de tutorías está funcionando correctamente con:
- Backend FastAPI con PostgreSQL
- Frontend React con login funcional
- Sistema de roles (admin/tutor)
- API REST completa
- Documentación automática

¡Disfruta usando tu aplicación! 🚀
