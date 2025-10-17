# Guía de Despliegue en AWS - Solo Amazon

## Arquitectura de Producción

- **Base de datos**: RDS PostgreSQL (db.t3.micro - free tier primer año)
- **Backend + Frontend**: AWS Amplify (todo en uno, deploy automático)
- **Costo**: ~$15-20/mes después del free tier (o ~$5-10/mes primer año)

## Paso 1: Crear Base de Datos RDS PostgreSQL

### 1.1 Crear instancia RDS
1. Ir a la consola de AWS RDS
2. Crear base de datos:
   - **Engine**: PostgreSQL 15
   - **Template**: Free tier
   - **DB instance identifier**: `tutorias-db`
   - **Master username**: `postgres`
   - **Master password**: `[CREAR_PASSWORD_SEGURA]`
   - **DB instance class**: `db.t3.micro` (free tier)
   - **Storage**: 20 GB (free tier)
   - **Public access**: Yes (para desarrollo)
3. **Security Group**: Crear nuevo grupo de seguridad que permita:
   - Puerto 5432 desde 0.0.0.0/0 (para desarrollo)
4. Crear base de datos

### 1.2 Obtener credenciales
- **Endpoint**: `xxx.xxxxx.us-east-1.rds.amazonaws.com`
- **Port**: `5432`
- **Database**: `postgres`
- **Username**: `postgres`
- **Password**: `[TU_PASSWORD]`

## Paso 2: Configurar Variables de Entorno

### 2.1 Crear archivo de configuración
1. Copiar `backend/env.aws.example` como `backend/.env.aws`
2. Reemplazar las credenciales:
   ```env
   DATABASE_URL=postgresql://postgres:[TU_PASSWORD]@[TU_ENDPOINT]:5432/postgres
   SECRET_KEY=tu-clave-secreta-super-segura-para-aws
   ALLOWED_ORIGINS=https://main.d1234567890.amplifyapp.com,http://localhost:5173,http://localhost:3000
   ```

### 2.2 Inicializar base de datos
```bash
cd backend
python init_rds.py
```

## Paso 3: Desplegar en AWS Amplify

### 3.1 Crear aplicación en Amplify
1. Ir a [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
2. **Host web app** → **GitHub**
3. Conectar con tu repositorio `app-tutorias`
4. Seleccionar rama `main`
5. Amplify detectará automáticamente la configuración

### 3.2 Configurar build settings
Amplify usará el archivo `amplify.yml` que ya está configurado:
- Frontend: npm ci → npm run build
- Backend: pip install → preparar para deploy

### 3.3 Configurar variables de entorno en Amplify
En la consola de Amplify, ir a **Environment variables**:
- `DATABASE_URL`: `postgresql://postgres:[PASSWORD]@[ENDPOINT]:5432/postgres`
- `SECRET_KEY`: `tu-clave-secreta-super-segura`
- `ALLOWED_ORIGINS`: `https://main.d1234567890.amplifyapp.com,http://localhost:5173`

### 3.4 Deploy automático
- Amplify desplegará automáticamente
- Generará URL como: `https://main.d1234567890.amplifyapp.com`

## Paso 4: Configuración Final

### 4.1 Actualizar CORS
1. Una vez que tengas la URL de Amplify
2. Actualizar `ALLOWED_ORIGINS` en Amplify console con la URL real
3. Hacer commit y push (deploy automático)

### 4.2 Probar aplicación
1. Ir a la URL de Amplify
2. Probar login con:
   - **Admin**: admin@tutorias.com / admin123
   - **Tutor Equipo A**: tutor1@tutorias.com / tutor123
   - **Tutor Equipo B**: tutor2@tutorias.com / tutor123

## URLs de Producción

- **Aplicación**: `https://main.d1234567890.amplifyapp.com`
- **Base de datos**: RDS Console en AWS
- **Logs**: Amplify Console → Build logs

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
- Amplify detectará los cambios
- Reconstruirá y redesplegará automáticamente
- No necesitas hacer nada más

## Monitoreo

- **Aplicación**: Amplify Console → Build history
- **Base de datos**: RDS Console → Monitoring
- **Logs**: Amplify Console → Logs

## Costos Estimados

### Con Free Tier (Primer Año):
- RDS db.t3.micro: $0 (750 horas/mes)
- RDS Storage 20GB: $0 (20GB free)
- Amplify Hosting: ~$5-10/mes
- **Total: ~$5-10/mes**

### Después de Free Tier:
- RDS db.t3.micro: ~$15/mes
- RDS Storage 20GB: ~$2/mes
- Amplify Hosting: ~$5-10/mes
- **Total: ~$15-20/mes**

## Escalabilidad Futura

Cuando pases a producción real:
1. **Base de datos**: Migrar a RDS Aurora Serverless v2
2. **Aplicación**: Mantener Amplify o migrar a ECS + CloudFront
3. **Monitoreo**: Agregar CloudWatch, X-Ray
4. **Seguridad**: WAF, Secrets Manager

## Troubleshooting

### Error de conexión a BD
- Verificar Security Group de RDS (puerto 5432 abierto)
- Verificar credenciales en variables de entorno
- Verificar que la BD esté inicializada

### Error de build en Amplify
- Verificar que `amplify.yml` esté en la raíz del proyecto
- Verificar que `requirements.txt` tenga todas las dependencias
- Revisar logs de build en Amplify Console

### Error de CORS
- Verificar que `ALLOWED_ORIGINS` incluya la URL de Amplify
- Verificar que no haya espacios en las URLs

## Ventajas de esta arquitectura:

- ✅ **TODO en AWS** (no dependencias externas)
- ✅ **MÁS SIMPLE**: Frontend y backend en un solo servicio
- ✅ **Deploy automático** con cada push
- ✅ **Free tier** el primer año
- ✅ **Escalable** para producción real
- ✅ **No necesitas Docker** ni App Runner
- ✅ **SSL automático** con Amplify
- ✅ **Monitoreo integrado** en AWS Console
