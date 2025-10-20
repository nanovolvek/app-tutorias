from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import auth_router, equipos_router, tutores_router, estudiantes_router, usuarios_router, attendance, tutor_attendance, attendance_2026
from app.database import engine, ALLOWED_ORIGINS
from app import models
import os

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Plataforma Tutorías API",
    description="API para la gestión de equipos, tutores y estudiantes",
    version="2.0.0"
)

# Health check endpoint para App Runner
@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Plataforma Tutorías API is running"}

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # URLs del frontend desde variables de entorno
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(auth_router)
app.include_router(equipos_router)
app.include_router(tutores_router)
app.include_router(estudiantes_router)
app.include_router(usuarios_router)
app.include_router(attendance.router)
app.include_router(tutor_attendance.router)
app.include_router(attendance_2026.router)

# Montar archivos estáticos del frontend
frontend_dist_path = "/app/static"
if os.path.exists(frontend_dist_path):
    # Montar archivos estáticos (CSS, JS, imágenes)
    app.mount("/assets", StaticFiles(directory=f"{frontend_dist_path}/assets"), name="assets")
    
    # Servir el archivo index.html para todas las rutas del frontend
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Si es una ruta de API, no servir el frontend
        if (full_path.startswith("api/") or 
            full_path.startswith("auth/") or 
            full_path.startswith("equipos/") or 
            full_path.startswith("tutores/") or 
            full_path.startswith("estudiantes/") or 
            full_path.startswith("usuarios/") or 
            full_path.startswith("attendance/") or 
            full_path.startswith("tutor-attendance/") or 
            full_path == "health"):
            return {"error": "Not found"}
        
        # Servir archivos estáticos específicos
        if full_path.endswith(('.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2')):
            file_path = os.path.join(frontend_dist_path, full_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return FileResponse(file_path)
        
        # Para todas las demás rutas del frontend (SPA), servir index.html
        index_path = os.path.join(frontend_dist_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        return {"error": "Not found"}

# Ruta raíz para servir el frontend React
@app.get("/")
async def serve_root():
    frontend_dist_path = "/app/static"
    index_path = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "¡Bienvenido a la Plataforma Tutorías API!"}
