# 🚀 Guía de Ejecución - Aplicación de Tutorías

## 📋 Resumen
Aplicación web completa de gestión de tutorías:
- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI + PostgreSQL
- **Autenticación:** JWT con roles (admin/tutor)

## 🗄️ Bases de Datos

### **Local vs Producción:**
- **Local:** PostgreSQL en tu máquina (`localhost:5432`)
- **Producción:** AWS RDS PostgreSQL (servidor remoto)

**⚠️ IMPORTANTE:** Son bases de datos completamente separadas. Los cambios locales NO afectan producción automáticamente.

## 🔧 Configuración Inicial

### 1. Prerrequisitos
- Node.js (v16+)
- Python (v3.8+)
- PostgreSQL local

### 2. Base de Datos Local
```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE tutorias_db;
\q
```

### 3. Backend
```bash
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt

# Configurar .env
DATABASE_URL=postgresql://postgres:nanopostgres@localhost:5432/tutorias_db
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Inicializar BD
python init_db.py

# Ejecutar
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend
```bash
# Nueva terminal
npm install
npm run dev
```

## 🚀 Flujo de Trabajo de Desarrollo

### **1. Antes de Empezar**
```bash
git pull origin main  # Siempre sincronizar con producción
```

### **2. Crear Rama para Cambios**
```bash
git checkout -b feature/nombre-de-tu-feature
# o
git checkout -b fix/descripcion-del-fix
```

### **3. Desarrollo Local**
- Modificar código frontend/backend
- Probar localmente en http://localhost:5173
- Verificar que todo funcione

### **4. Cambios en Base de Datos**
```bash
# Crear migración
cd backend
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migración local
alembic upgrade head
```

### **5. Confirmar Cambios**
```bash
git add .
git commit -m "feat: Descripción del cambio"
git push origin feature/nombre-de-tu-feature
```

### **6. Desplegar a Producción**
```bash
# Fusionar con main
git checkout main
git merge feature/nombre-de-tu-feature
git push origin main

# AWS App Runner se encarga del despliegue automático
```

## 🔑 Credenciales de Prueba

- **Admin:** `admin@tutorias.com` / `admin`
- **Tutor:** `tutor@tutorias.com` / `tutor`

## 🌐 URLs

- **Local Frontend:** http://localhost:5173
- **Local Backend:** http://localhost:8000
- **Producción Frontend:** https://main.d1d2p1x4drhejl.amplifyapp.com
- **Producción Backend:** https://wh7jum5qhe.us-east-1.awsapprunner.com

## ⚠️ Reglas Importantes

1. **NUNCA trabajes directamente en `main`**
2. **Siempre sincroniza con `main` antes de empezar**
3. **Prueba todo localmente antes de subir**
4. **Para cambios de BD, crea migraciones de Alembic**
5. **Haz commits descriptivos** (`feat:`, `fix:`, `docs:`)

## 🚨 Solución de Problemas

### Error de conexión a BD
- Verificar que PostgreSQL esté corriendo
- Verificar credenciales en `.env`

### Error de CORS
- Backend en puerto 8000
- Frontend en puerto 5173

### Error de TypeScript
- Verificar que no hay variables no utilizadas
- Ejecutar `npm run build` para verificar

## 📝 Comandos Rápidos

```bash
# Iniciar todo
# Terminal 1
cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2
npm run dev

# Verificar puertos
netstat -an | findstr ":8000\|:5173"
```

## ✅ Verificación Final

1. ✅ Login funcional en http://localhost:5173
2. ✅ Dashboard con información del usuario
3. ✅ Navegación entre secciones
4. ✅ API funcionando en http://localhost:8000/docs

¡Listo para desarrollar! 🎉

## 🔄 Flujo de Trabajo para Desarrollo y Producción

### **Desarrollo Local (Sin cambios de BD)**
```bash
# 1. Crear rama
git checkout -b feature/nueva-funcionalidad

# 2. Desarrollar localmente
# ... hacer cambios en código ...

# 3. Probar localmente
npm run dev  # frontend
python -m uvicorn app.main:app --reload  # backend

# 4. Commit y push
git add .
git commit -m "feat: Nueva funcionalidad"
git push origin feature/nueva-funcionalidad

# 5. Merge a main
git checkout main
git merge feature/nueva-funcionalidad
git push origin main

# 6. AWS App Runner despliega automáticamente
```

### **Cambios de Base de Datos (CRÍTICO)**

#### **Opción A: Migraciones (Recomendado)**
```bash
# 1. Crear migración para el cambio
cd backend
alembic revision --autogenerate -m "Descripción del cambio"

# 2. Probar migración localmente
alembic upgrade head

# 3. Commit de la migración
git add alembic/versions/
git commit -m "feat: Agregar migración para cambio de BD"

# 4. Deploy a producción
git push origin main

# 5. AWS App Runner aplica la migración automáticamente
```

#### **Opción B: Scripts de Datos (Para datos de prueba)**
```bash
# 1. Crear script de datos
# backend/scripts/init_prod_data.py

# 2. Ejecutar solo en producción (una vez)
# AWS App Runner ejecuta el script al desplegar
```

## 🚨 Reglas de Oro

### **✅ SÍ hacer:**
- Desarrollar localmente
- Usar migraciones para cambios de BD
- Commit código y migraciones
- Deploy automático

### **❌ NO hacer:**
- Sincronizar BD local → producción
- Modificar producción directamente
- Commit datos reales

### **Separación de Entornos:**
- **Local:** Para desarrollo y testing
- **Producción:** Solo para datos reales de usuarios

## 🔧 Sincronización de Datos

### **Para obtener datos de producción en local:**
```bash
# Usar el script de sincronización (solo cuando sea necesario)
python sync_prod_to_local.py
```

### **Para cambios de datos de prueba:**
1. Modificar datos localmente
2. Crear script de inicialización
3. Commit script (no los datos)
4. Deploy → Script se ejecuta en producción

## 📋 Resumen del Flujo

1. **Desarrollo:** Trabaja localmente con BD local
2. **Testing:** Prueba todo en tu entorno local
3. **Código:** Commit solo código (no datos)
4. **BD:** Usa migraciones para cambios estructurales
5. **Deploy:** Push a GitHub → AWS App Runner despliega automáticamente