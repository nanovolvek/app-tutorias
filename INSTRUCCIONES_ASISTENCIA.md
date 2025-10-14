# Instrucciones para la Funcionalidad de Asistencia

## Resumen de la Implementación

Se ha implementado un sistema completo de seguimiento de asistencia que incluye:

1. **Modelo de Base de Datos**: Tabla `attendance` con 10 semanas de seguimiento
2. **API Backend**: Endpoints para gestionar y consultar asistencia
3. **Frontend**: Gráfico interactivo y tabla de asistencia en el Dashboard

## Archivos Creados/Modificados

### Backend
- `backend/app/models/attendance.py` - Modelo de asistencia
- `backend/app/schemas/attendance.py` - Esquemas Pydantic
- `backend/app/routers/attendance.py` - Endpoints de la API
- `backend/app/models/student.py` - Agregada relación con asistencia
- `backend/app/models/__init__.py` - Importación del modelo
- `backend/app/schemas/__init__.py` - Importación de esquemas
- `backend/app/routers/__init__.py` - Importación del router
- `backend/app/main.py` - Incluido router de asistencia
- `backend/init_attendance_data.py` - Script para datos de prueba
- `backend/run_migration.py` - Script para migración

### Frontend
- `src/components/AttendanceChart.tsx` - Componente de gráfico
- `src/components/AttendanceChart.css` - Estilos del gráfico
- `src/pages/Dashboard.tsx` - Integración del gráfico
- `package.json` - Agregadas dependencias de Chart.js

## Pasos para Probar la Funcionalidad

### 1. Configurar el Backend

```bash
cd backend

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias (si no están instaladas)
pip install -r requirements.txt

# Ejecutar migración para crear la tabla de asistencia
python run_migration.py

# Inicializar datos de prueba de asistencia
python init_attendance_data.py

# Iniciar el servidor backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Configurar el Frontend

```bash
# En otra terminal, desde la raíz del proyecto
npm install
npm run dev
```

### 3. Probar la Funcionalidad

1. **Acceder al Dashboard**: Ve a `http://localhost:5173` y haz login
2. **Ver el Gráfico**: En el Dashboard verás:
   - Un gráfico de barras mostrando el % de asistencia por estudiante
   - Una tabla detallada con el estado de asistencia por semana
   - Colores que indican el nivel de asistencia (verde ≥80%, amarillo ≥60%, rojo <60%)

## Endpoints de la API

### GET `/attendance/summary`
Obtiene el resumen de asistencia de todos los estudiantes con porcentajes.

**Respuesta:**
```json
[
  {
    "student_id": 1,
    "student_name": "Juan Pérez",
    "course": "3° Básico",
    "school_name": "Colegio San Patricio",
    "total_weeks": 10,
    "attended_weeks": 7,
    "attendance_percentage": 70.0,
    "weekly_attendance": {
      "semana_1": true,
      "semana_2": false,
      "semana_3": true,
      ...
    }
  }
]
```

### POST `/attendance/`
Crear o actualizar un registro de asistencia.

**Body:**
```json
{
  "student_id": 1,
  "week": "semana_1",
  "attended": true
}
```

### PUT `/attendance/{attendance_id}`
Actualizar un registro de asistencia existente.

**Body:**
```json
{
  "attended": true
}
```

### POST `/attendance/initialize/{student_id}`
Inicializar registros de asistencia para un estudiante (10 semanas).

## Características del Gráfico

- **Gráfico de Barras**: Muestra el porcentaje de asistencia por estudiante
- **Colores Dinámicos**: 
  - Verde: ≥80% de asistencia
  - Amarillo: 60-79% de asistencia
  - Rojo: <60% de asistencia
- **Tooltip Informativo**: Al pasar el mouse muestra detalles del estudiante
- **Tabla Detallada**: Muestra el estado de asistencia semana por semana
- **Responsive**: Se adapta a diferentes tamaños de pantalla

## Datos de Prueba

El script `init_attendance_data.py` genera datos aleatorios de asistencia:
- Cada estudiante tiene registros para 10 semanas
- Probabilidad del 70% de asistir en cada semana
- Los datos se generan de forma aleatoria pero consistente

## Notas Técnicas

- La tabla `attendance` se crea automáticamente al ejecutar la migración
- Los datos de asistencia se inicializan solo si no existen
- El frontend maneja estados de carga y error apropiadamente
- El gráfico es interactivo y se actualiza automáticamente
- Los estilos son responsive y modernos
