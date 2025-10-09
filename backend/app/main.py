from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, schools, tutors, students
from app.database import engine
from app import models

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Plataforma Tutorías API",
    description="API para la gestión de tutores, estudiantes y colegios",
    version="1.0.0"
)

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # URLs del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(auth.router)
app.include_router(schools.router)
app.include_router(tutors.router)
app.include_router(students.router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la Plataforma Tutorías API!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}
