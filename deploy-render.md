# 🚀 Despliegue en Render.com

## Pasos para desplegar en Render.com:

### 1. Crear cuenta en Render.com
- Ve a [render.com](https://render.com)
- Regístrate con tu cuenta de GitHub

### 2. Conectar repositorio
- Haz clic en "New +" → "Web Service"
- Conecta tu repositorio: `nanovolvek/app-tutorias`
- Selecciona la rama: `main`

### 3. Configurar el servicio
- **Name**: `tutorias-app`
- **Environment**: `Docker`
- **Dockerfile Path**: `./Dockerfile`
- **Plan**: `Free`

### 4. Configurar variables de entorno
- `DATABASE_URL`: (se configurará automáticamente)
- `SECRET_KEY`: `tutorias-render-secret-key-2025`
- `ALLOWED_ORIGINS`: `https://tutorias-app.onrender.com,http://localhost:5173`

### 5. Crear base de datos PostgreSQL
- Haz clic en "New +" → "PostgreSQL"
- **Name**: `tutorias-db`
- **Plan**: `Free`
- **Region**: `Oregon (US West)`

### 6. Conectar base de datos
- En el servicio web, ve a "Environment"
- Agrega la variable `DATABASE_URL` desde la base de datos

### 7. Desplegar
- Haz clic en "Deploy"
- Espera a que termine la construcción (5-10 minutos)

## ✅ Resultado esperado:
- **Frontend**: https://tutorias-app.onrender.com
- **Backend API**: https://tutorias-app.onrender.com/health
- **Base de datos**: PostgreSQL en Render

## 🔧 Comandos útiles:
```bash
# Ver logs
render logs --service tutorias-app

# Ver estado
render status

# Reiniciar servicio
render restart --service tutorias-app
```
