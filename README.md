# 🎓 Plataforma de Tutorías - Sistema Completo

## 📋 Descripción
Sistema web completo para gestión de tutorías escolares con autenticación, gestión de equipos, tutores, estudiantes y control de asistencias.

## 🏗️ Arquitectura
- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + Python
- **Base de Datos**: PostgreSQL
- **Despliegue**: Render.com (Docker)
- **Autenticación**: JWT con roles (admin/tutor)

## 🗄️ Bases de Datos

### **Local (Desarrollo)**
- **Ubicación**: Tu máquina local
- **Host**: `localhost:5432`
- **Base de datos**: `tutorias_db`
- **Usuario**: `postgres`
- **Contraseña**: `nanopostgres`
- **Propósito**: Desarrollo y pruebas

### **Producción (Render)**
- **Ubicación**: Render.com (Oregon, US West)
- **Host**: `dpg-d3pr88c9c44c73c9snsg-a.oregon-postgres.render.com`
- **Base de datos**: `tutorias_db`
- **Usuario**: `tutorias_db_user`
- **Propósito**: Aplicación en vivo

**⚠️ IMPORTANTE**: Son bases de datos completamente separadas. Los cambios locales NO afectan producción automáticamente.

## 🚀 Despliegue en Render.com

### **URL de Producción**
- **Aplicación**: https://app-tutorias.onrender.com
- **API**: https://app-tutorias.onrender.com/health

### **Credenciales de Prueba**
- **Admin**: `admin@tutorias.com` / `admin123`
- **Tutor A**: `tutor1@tutorias.com` / `tutor123`
- **Tutor B**: `tutor2@tutorias.com` / `tutor123`

## 🔧 Configuración Local

### **Prerrequisitos**
- Node.js (v18+)
- Python (v3.9+)
- PostgreSQL local
- Git

### **1. Clonar y Configurar**
```bash
git clone https://github.com/nanovolvek/app-tutorias.git
cd app-tutorias
```

### **2. Base de Datos Local**
```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE tutorias_db;
\q
```

### **3. Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

# Configurar variables de entorno
# Crear archivo .env con:
DATABASE_URL=postgresql://postgres:nanopostgres@localhost:5432/tutorias_db
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Inicializar base de datos
python init_db.py

# Ejecutar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **4. Frontend**
```bash
# En otra terminal
npm install
npm run dev
```

### **5. Acceder a la Aplicación**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 🔄 Flujo de Trabajo Recomendado

### **1. Desarrollo Local**
1. **Hacer cambios** en el código local
2. **Probar** en http://localhost:5173
3. **Verificar** que todo funciona correctamente
4. **Probar** con la base de datos local

### **2. Sincronizar con Producción**
1. **Hacer commit** de los cambios:
   ```bash
   git add .
   git commit -m "Descripción del cambio"
   git push origin main
   ```

2. **Render detecta** el cambio automáticamente y hace deploy

3. **Sincronizar base de datos** (si es necesario):
   ```bash
   python migrate_local_to_render_final.py
   ```

### **3. Verificar Producción**
1. **Probar** en https://app-tutorias.onrender.com
2. **Verificar** que los cambios funcionan
3. **Revisar logs** en Render si hay problemas

## 🗄️ Gestión de Base de Datos

### **Conectar con DBeaver**

#### **Base de Datos Local**
- **Host**: `localhost`
- **Puerto**: `5432`
- **Base de datos**: `tutorias_db`
- **Usuario**: `postgres`
- **Contraseña**: `nanopostgres`

#### **Base de Datos de Producción**
- **Host**: `dpg-d3pr88c9c44c73c9snsg-a.oregon-postgres.render.com`
- **Puerto**: `5432`
- **Base de datos**: `tutorias_db`
- **Usuario**: `tutorias_db_user`
- **Contraseña**: `kDL6FlvxRo9urc0X7DHUi86RHi0F2ec2`
- **SSL**: Requerido

### **Migrar Datos de Local a Producción**
```bash
# Ejecutar script de migración
python migrate_local_to_render_final.py
```

## 📁 Estructura del Proyecto

```
app-tutorias/
├── src/                    # Frontend React
│   ├── components/         # Componentes reutilizables
│   ├── pages/             # Páginas principales
│   ├── contexts/          # Contextos de React
│   └── hooks/             # Hooks personalizados
├── backend/               # Backend FastAPI
│   ├── app/
│   │   ├── models/        # Modelos de base de datos
│   │   ├── routers/       # Rutas de la API
│   │   ├── schemas/       # Esquemas Pydantic
│   │   └── auth/          # Autenticación
│   └── requirements.txt   # Dependencias Python
├── Dockerfile            # Configuración Docker
├── docker-compose.yml    # Desarrollo local con Docker
├── render.yaml          # Configuración Render.com
└── migrate_local_to_render_final.py  # Script de migración
```

## 🚨 Solución de Problemas

### **Error de Conexión a Base de Datos**
1. Verificar que PostgreSQL esté ejecutándose
2. Verificar credenciales en `.env`
3. Verificar que la base de datos `tutorias_db` existe

### **Error de Login en Producción**
1. Verificar que la base de datos de producción tenga usuarios
2. Ejecutar script de migración si es necesario
3. Verificar logs en Render

### **Frontend no Carga**
1. Verificar que el backend esté ejecutándose
2. Verificar que la URL de la API sea correcta
3. Verificar logs del navegador

## 📞 Soporte
- **GitHub**: https://github.com/nanovolvek/app-tutorias
- **Render Dashboard**: https://dashboard.render.com
- **Documentación API**: https://app-tutorias.onrender.com/docs

## 🔐 Seguridad
- Las contraseñas están hasheadas con bcrypt
- Los tokens JWT tienen expiración de 30 minutos
- Las conexiones a la base de datos usan SSL en producción
- Las variables de entorno están protegidas

## 📈 Próximos Pasos
1. **Upgrade a plan pago** en Render para eliminar delays
2. **Configurar backup** automático de la base de datos
3. **Implementar monitoreo** de la aplicación
4. **Agregar tests** automatizados
