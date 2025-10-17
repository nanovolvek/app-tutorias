# Guía de Despliegue a Producción

## Arquitectura de Producción

- **Backend**: AWS App Runner (despliegue automático desde GitHub)
- **Frontend**: Vercel (despliegue automático desde GitHub)
- **Base de datos**: Supabase (gratis hasta 500MB)

## Costos Estimados

- Supabase: $0 (tier gratuito - 500MB)
- Vercel: $0 (tier gratuito)
- AWS App Runner: ~$5-10/mes (0.007 USD/hora + $0.064/GB tráfico)
- **Total: ~$5-10/mes**

## Paso 1: Configurar Supabase

### 1.1 Crear proyecto en Supabase
1. Ir a [supabase.com](https://supabase.com)
2. Crear cuenta y nuevo proyecto
3. Anotar las credenciales de conexión:
   - Host: `[YOUR_PROJECT_REF].supabase.co`
   - Database: `postgres`
   - User: `postgres`
   - Password: `[YOUR_PASSWORD]`
   - Port: `5432`

### 1.2 Configurar variables de entorno
1. Copiar `backend/env.production.example` como `backend/.env.production`
2. Reemplazar las credenciales de Supabase:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@[YOUR_PROJECT_REF].supabase.co:5432/postgres
   SECRET_KEY=tu-clave-secreta-super-segura
   ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
   ```

### 1.3 Inicializar base de datos
```bash
cd backend
python init_supabase.py
```

## Paso 2: Desplegar Backend en AWS App Runner

### 2.1 Configurar App Runner
1. Ir a la consola de AWS App Runner
2. Crear nuevo servicio
3. Conectar con GitHub:
   - Repositorio: `tu-usuario/app-tutorias`
   - Rama: `main`
   - Directorio: `backend/`
4. Configurar build:
   - Runtime: Docker
   - Dockerfile: `backend/Dockerfile`
5. Configurar variables de entorno:
   - `DATABASE_URL`: URL de Supabase
   - `SECRET_KEY`: Clave secreta
   - `ALLOWED_ORIGINS`: `http://localhost:5173,http://localhost:3000` (se actualizará después)

### 2.2 Obtener URL del backend
- App Runner generará una URL como: `https://xxxxx.us-east-1.awsapprunner.com`
- Anotar esta URL para configurar el frontend

## Paso 3: Desplegar Frontend en Vercel

### 3.1 Configurar Vercel
1. Ir a [vercel.com](https://vercel.com)
2. Conectar con GitHub
3. Importar proyecto `app-tutorias`
4. Configurar build:
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Configurar variables de entorno:
   - `VITE_API_URL`: URL del backend de App Runner

### 3.2 Obtener URL del frontend
- Vercel generará una URL como: `https://app-tutorias-xxxxx.vercel.app`
- Anotar esta URL

## Paso 4: Configuración Final

### 4.1 Actualizar CORS en backend
1. Actualizar `backend/.env.production`:
   ```env
   ALLOWED_ORIGINS=https://app-tutorias-xxxxx.vercel.app,http://localhost:5173,http://localhost:3000
   ```
2. Hacer commit y push (deploy automático)

### 4.2 Probar aplicación
1. Ir a la URL del frontend
2. Probar login con:
   - **Admin**: admin@tutorias.com / admin123
   - **Tutor Equipo A**: tutor1@tutorias.com / tutor123
   - **Tutor Equipo B**: tutor2@tutorias.com / tutor123

## URLs de Producción

- **Frontend**: `https://app-tutorias-xxxxx.vercel.app`
- **Backend**: `https://xxxxx.us-east-1.awsapprunner.com`
- **Base de datos**: Supabase Dashboard

## Credenciales de Acceso

### Usuarios de prueba:
- **Administrador**: admin@tutorias.com / admin123
- **Tutor Equipo A**: tutor1@tutorias.com / tutor123
- **Tutor Equipo B**: tutor2@tutorias.com / tutor123

### Funcionalidades por rol:
- **Admin**: Ve todos los equipos, tutores y estudiantes
- **Tutores**: Solo ven información de su equipo asignado

## Deploy Automático

Cada vez que hagas push a la rama `main`:
1. **Backend**: Se despliega automáticamente en AWS App Runner
2. **Frontend**: Se despliega automáticamente en Vercel

## Monitoreo

- **Backend**: Logs en AWS App Runner console
- **Base de datos**: Dashboard de Supabase
- **Frontend**: Analytics en Vercel dashboard

## Escalabilidad Futura

Cuando pases a producción real:
1. **Base de datos**: Migrar a RDS PostgreSQL (más robusto)
2. **Backend**: Mantener App Runner o migrar a ECS
3. **Frontend**: Mantener Vercel o migrar a CloudFront + S3
4. **Monitoreo**: Agregar CloudWatch, Sentry, etc.

## Troubleshooting

### Error de CORS
- Verificar que `ALLOWED_ORIGINS` incluya la URL de Vercel
- Reiniciar el servicio de App Runner

### Error de conexión a BD
- Verificar credenciales en Supabase
- Verificar que la BD esté inicializada con `init_supabase.py`

### Error de build
- Verificar que todas las dependencias estén en `requirements.txt`
- Verificar que el Dockerfile esté correcto
