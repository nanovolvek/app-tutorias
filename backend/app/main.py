from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, equipos_router, tutores_router, estudiantes_router, usuarios_router
from app.database import engine, ALLOWED_ORIGINS
from app import models

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Plataforma Tutorías API",
    description="API para la gestión de equipos, tutores y estudiantes",
    version="2.0.0"
)

# Health check endpoint para App Runner
@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "Plataforma Tutorías API is running"}

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

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la Plataforma Tutorías API!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}
