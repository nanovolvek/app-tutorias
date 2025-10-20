# 📅 SISTEMA DE ASISTENCIA 2026 - GUÍA DE IMPLEMENTACIÓN

## 🎯 OBJETIVO
Implementar un sistema de asistencia completo para el año 2026 que permita:
- Registrar asistencia de estudiantes y tutores por semana
- Filtrar por mes, colegio y equipo
- Visualizar datos en formato tabla
- Actualizar estados de asistencia en tiempo real

## 📋 ESTADO ACTUAL DE LA BASE DE DATOS

### ✅ Tablas Existentes
- `asistencia_estudiantes` - ✅ Existe con campos: `id`, `estudiante_id`, `semana`, `mes`, `dias`, `estado`
- `asistencia_tutores` - ✅ Existe con campos: `id`, `tutor_id`, `semana`, `mes`, `dias`, `estado`
- `estudiantes` - ✅ Existe con relación a `equipos`
- `tutores` - ✅ Existe con relación a `equipos`
- `equipos` - ✅ Existe con relación a `colegios`
- `colegios` - ✅ Existe

### 📊 Datos Actuales
- **645 registros** de asistencia en la base de datos
- **15 estudiantes** registrados
- **43 semanas** de datos (desde marzo hasta diciembre 2026)
- **Estados disponibles**: `asistió`, `no asistió`, `tutoría suspendida`, `vacaciones/feriado`

## 🔧 PLAN DE IMPLEMENTACIÓN PASO A PASO

### **FASE 1: Preparación del Backend** ⚠️ CRÍTICO

#### 1.1 Verificar Modelos Existentes
```bash
# Verificar que los modelos coincidan con la base de datos
cd backend
python -c "
from app.database import get_db
from app.models.attendance import AsistenciaEstudiante, AsistenciaTutor
db = next(get_db())
print('Estudiantes:', db.query(AsistenciaEstudiante).count())
print('Tutores:', db.query(AsistenciaTutor).count())
"
```

#### 1.2 Actualizar Modelos (SI ES NECESARIO)
- **NO cambiar** los modelos si ya coinciden con la base de datos
- **Solo agregar** campos si faltan
- **Mantener** la estructura existente

#### 1.3 Crear Router de Asistencia
```python
# backend/app/routers/attendance_2026.py
# Endpoints necesarios:
# - GET /attendance-2026/calendar/weeks (calendario 2026)
# - GET /attendance-2026/students?month=X (estudiantes por mes)
# - GET /attendance-2026/tutors?month=X (tutores por mes)
# - POST /attendance-2026/students (crear/actualizar asistencia estudiante)
# - POST /attendance-2026/tutors (crear/actualizar asistencia tutor)
```

#### 1.4 Crear Calendario 2026
```python
# backend/generate_2026_calendar.py
# Generar archivo JSON con 43 semanas desde marzo hasta diciembre
```

### **FASE 2: Testing del Backend** 🧪

#### 2.1 Probar Endpoints Individualmente
```bash
# 1. Probar calendario
curl http://localhost:8000/attendance-2026/calendar/weeks

# 2. Probar login
python -c "
import requests
login_data = {'email': 'admin@tutorias.com', 'password': 'admin123'}
response = requests.post('http://localhost:8000/auth/login-json', json=login_data)
print('Login:', response.status_code)
"

# 3. Probar endpoint de estudiantes
python -c "
import requests
headers = {'Authorization': 'Bearer TOKEN_AQUI'}
response = requests.get('http://localhost:8000/attendance-2026/students?month=Marzo', headers=headers)
print('Students:', response.status_code)
"
```

#### 2.2 Verificar Datos de Respuesta
- ✅ Calendario devuelve 43 semanas
- ✅ Estudiantes devuelve lista con datos reales
- ✅ Tutores devuelve lista con datos reales
- ✅ Estados de asistencia se actualizan correctamente

### **FASE 3: Frontend** 🎨

#### 3.1 Actualizar Componente Asistencia
```typescript
// src/pages/Asistencia.tsx
// Cambios necesarios:
// 1. Conectar con API real en lugar de datos mock
// 2. Implementar filtros por mes, colegio, equipo
// 3. Mostrar tabla con semanas como columnas
// 4. Permitir actualización de estados
```

#### 3.2 Funciones Principales
```typescript
// Funciones que necesitan implementación:
const fetchCalendar = async () => { /* Cargar calendario desde API */ }
const fetchStudents = async (month, schoolId, equipoId) => { /* Cargar estudiantes */ }
const fetchTutors = async (month, schoolId, equipoId) => { /* Cargar tutores */ }
const updateAttendance = async (personId, week, status) => { /* Actualizar asistencia */ }
```

### **FASE 4: Integración y Testing** 🔗

#### 4.1 Testing Completo
1. **Login** → ✅ Funciona
2. **Cargar calendario** → ✅ Funciona
3. **Filtrar por mes** → ✅ Funciona
4. **Mostrar estudiantes/tutores** → ✅ Funciona
5. **Actualizar asistencia** → ✅ Funciona
6. **Persistir cambios** → ✅ Funciona

#### 4.2 Verificar Funcionalidades
- ✅ Dropdown de colegios se llena
- ✅ Dropdown de equipos se llena
- ✅ Tabla se actualiza al cambiar filtros
- ✅ Estados se guardan en base de datos
- ✅ Cambios persisten al recargar

## ⚠️ REGLAS CRÍTICAS

### **NO HACER**
- ❌ Cambiar modelos existentes sin verificar
- ❌ Modificar estructura de base de datos
- ❌ Implementar todo de una vez
- ❌ Hacer cambios sin probar cada paso

### **SÍ HACER**
- ✅ Probar cada endpoint individualmente
- ✅ Verificar que los datos existentes no se rompan
- ✅ Implementar paso a paso
- ✅ Hacer rollback si algo falla
- ✅ Mantener compatibilidad con código existente

## 🚨 PUNTOS DE FALLA COMUNES

### 1. **Errores de Importación**
```python
# PROBLEMA: ImportError: cannot import name 'School'
# SOLUCIÓN: Usar alias en modelos
# School = Colegio
# User = Usuario
```

### 2. **Errores de CORS**
```python
# PROBLEMA: CORS policy blocks requests
# SOLUCIÓN: Verificar ALLOWED_ORIGINS en database.py
ALLOWED_ORIGINS = "http://localhost:5173,http://localhost:3000"
```

### 3. **Errores de Base de Datos**
```python
# PROBLEMA: Modelo no coincide con tabla
# SOLUCIÓN: Verificar estructura real de la base de datos
# NO cambiar modelos sin confirmar estructura
```

### 4. **Errores de Router**
```python
# PROBLEMA: Router no se incluye en main.py
# SOLUCIÓN: Agregar router paso a paso
app.include_router(attendance_2026.router)
```

## 📝 CHECKLIST DE IMPLEMENTACIÓN

### Backend
- [ ] Verificar modelos existentes
- [ ] Crear router attendance_2026.py
- [ ] Generar calendario 2026
- [ ] Probar endpoint de calendario
- [ ] Probar endpoint de estudiantes
- [ ] Probar endpoint de tutores
- [ ] Probar actualización de asistencia
- [ ] Incluir router en main.py

### Frontend
- [ ] Conectar con API real
- [ ] Implementar filtros
- [ ] Mostrar tabla de asistencia
- [ ] Implementar actualización de estados
- [ ] Probar funcionalidad completa

### Testing
- [ ] Login funciona
- [ ] Calendario se carga
- [ ] Filtros funcionan
- [ ] Datos se muestran correctamente
- [ ] Actualizaciones se guardan
- [ ] Cambios persisten

## 🎯 RESULTADO FINAL

Un sistema de asistencia completamente funcional que:
- ✅ Muestra datos reales de la base de datos
- ✅ Permite filtrar por mes, colegio y equipo
- ✅ Actualiza estados en tiempo real
- ✅ Persiste cambios en la base de datos
- ✅ Mantiene compatibilidad con el sistema existente

## 📞 SOPORTE

Si algo falla:
1. **Hacer rollback** inmediatamente
2. **Verificar logs** del servidor
3. **Probar endpoints** individualmente
4. **Implementar paso a paso** más lentamente
5. **Mantener sistema básico** funcionando

---

**IMPORTANTE**: Este sistema debe implementarse gradualmente para evitar romper la funcionalidad existente. Cada paso debe probarse antes de continuar.
