from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models.tickets import TicketEstudiante, EstadoTicket
from app.models.student import Estudiante
from app.models.equipo import Equipo
from app.models.school import Colegio
from app.auth.dependencies import get_current_user
from pydantic import BaseModel
import json

router = APIRouter()

# Esquemas Pydantic
class TicketUpdateRequest(BaseModel):
    student_id: int
    unidad: str
    modulo: str
    resultado: str

# Datos de módulos por unidad (5 módulos por cada una de las 5 unidades)
MODULOS_DATA = {
    "unidad_1": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 1", "descripcion": "Fundamentos básicos"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 2", "descripcion": "Conceptos intermedios"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 3", "descripcion": "Aplicaciones prácticas"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 4", "descripcion": "Análisis avanzado"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 5", "descripcion": "Síntesis y evaluación"}
    ],
    "unidad_2": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 1", "descripcion": "Fundamentos básicos"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 2", "descripcion": "Conceptos intermedios"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 3", "descripcion": "Aplicaciones prácticas"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 4", "descripcion": "Análisis avanzado"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 5", "descripcion": "Síntesis y evaluación"}
    ],
    "unidad_3": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 1", "descripcion": "Fundamentos básicos"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 2", "descripcion": "Conceptos intermedios"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 3", "descripcion": "Aplicaciones prácticas"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 4", "descripcion": "Análisis avanzado"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 5", "descripcion": "Síntesis y evaluación"}
    ],
    "unidad_4": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 1", "descripcion": "Fundamentos básicos"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 2", "descripcion": "Conceptos intermedios"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 3", "descripcion": "Aplicaciones prácticas"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 4", "descripcion": "Análisis avanzado"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 5", "descripcion": "Síntesis y evaluación"}
    ],
    "unidad_5": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 1", "descripcion": "Fundamentos básicos"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 2", "descripcion": "Conceptos intermedios"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 3", "descripcion": "Aplicaciones prácticas"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 4", "descripcion": "Análisis avanzado"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 5", "descripcion": "Síntesis y evaluación"}
    ]
}

@router.get("/unidades")
def get_unidades(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener lista de unidades disponibles"""
    try:
        unidades = [
            {"unidad_key": "unidad_1", "nombre": "Unidad 1", "descripcion": "Primera unidad del programa"},
            {"unidad_key": "unidad_2", "nombre": "Unidad 2", "descripcion": "Segunda unidad del programa"},
            {"unidad_key": "unidad_3", "nombre": "Unidad 3", "descripcion": "Tercera unidad del programa"},
            {"unidad_key": "unidad_4", "nombre": "Unidad 4", "descripcion": "Cuarta unidad del programa"},
            {"unidad_key": "unidad_5", "nombre": "Unidad 5", "descripcion": "Quinta unidad del programa"}
        ]
        return {"unidades": unidades}
    except Exception as e:
        print(f"Error en get_unidades: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/modulos")
def get_modulos(
    unidad: Optional[str] = Query(None, description="Unidad para obtener módulos"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener módulos de una unidad específica"""
    try:
        if not unidad:
            return {"modulos": []}
        
        if unidad not in MODULOS_DATA:
            raise HTTPException(status_code=400, detail="Unidad no válida")
        
        return {"modulos": MODULOS_DATA[unidad]}
    except Exception as e:
        print(f"Error en get_modulos: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/students")
def get_students_tickets(
    unidad: Optional[str] = Query(None, description="Unidad para filtrar"),
    equipo_id: Optional[int] = Query(None, description="ID del equipo"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener tickets de estudiantes con filtros"""
    try:
        if not unidad:
            raise HTTPException(status_code=400, detail="Unidad es requerida")
        
        # Construir query base
        query = db.query(Estudiante).join(Equipo).join(Colegio)
        
        # Aplicar filtros según el rol del usuario
        if current_user.rol == 'tutor':
            # Tutor solo ve estudiantes de su equipo
            query = query.filter(Estudiante.equipo_id == current_user.equipo_id)
        elif current_user.rol == 'admin' and equipo_id:
            # Admin puede filtrar por equipo específico
            query = query.filter(Estudiante.equipo_id == equipo_id)
        
        estudiantes = query.all()
        
        # Obtener módulos de la unidad
        modulos = MODULOS_DATA.get(unidad, [])
        
        # Construir respuesta con datos de tickets
        students_data = []
        for estudiante in estudiantes:
            # Obtener tickets existentes para esta unidad
            tickets_existentes = db.query(TicketEstudiante).filter(
                TicketEstudiante.estudiante_id == estudiante.id,
                TicketEstudiante.unidad == unidad
            ).all()
            
            # Crear diccionario de tickets por módulo
            tickets_por_modulo = {}
            for ticket in tickets_existentes:
                tickets_por_modulo[ticket.modulo] = ticket.resultado.value if ticket.resultado else "vacío"
            
            # Crear estructura de datos del estudiante
            student_data = {
                "id": estudiante.id,
                "nombre": estudiante.nombre,
                "apellido": estudiante.apellido,
                "equipo_id": estudiante.equipo_id,
                "colegio_nombre": estudiante.equipo.colegio.nombre if estudiante.equipo.colegio else "Sin colegio",
                "tickets": {}
            }
            
            # Agregar tickets para cada módulo
            for modulo in modulos:
                modulo_key = modulo["modulo_key"]
                student_data["tickets"][modulo_key] = tickets_por_modulo.get(modulo_key, "vacío")
            
            students_data.append(student_data)
        
        return {
            "unidad": unidad,
            "modulos": modulos,
            "students": students_data
        }
        
    except Exception as e:
        print(f"Error en get_students_tickets: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/equipos")
def get_equipos_list(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener lista de equipos con sus colegios para filtros"""
    try:
        equipos = db.query(Equipo).join(Colegio).all()
        return [
            {
                "id": equipo.id,
                "nombre": equipo.nombre,
                "colegio_id": equipo.colegio_id,
                "colegio_nombre": equipo.colegio.nombre if equipo.colegio else "Sin colegio"
            }
            for equipo in equipos
        ]
    except Exception as e:
        print(f"Error en get_equipos_list: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/students")
def update_student_ticket(
    request: TicketUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear o actualizar ticket de estudiante"""
    
    # Verificar que el estudiante existe
    student = db.query(Estudiante).filter(Estudiante.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Verificar permisos del tutor
    if current_user.rol == 'tutor' and student.equipo_id != current_user.equipo_id:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar este estudiante")
    
    # Verificar que el resultado es válido
    try:
        resultado_enum = EstadoTicket(request.resultado)
    except ValueError:
        raise HTTPException(status_code=400, detail="Resultado de ticket inválido")
    
    # Buscar registro existente
    existing_record = db.query(TicketEstudiante).filter(
        TicketEstudiante.estudiante_id == request.student_id,
        TicketEstudiante.unidad == request.unidad,
        TicketEstudiante.modulo == request.modulo
    ).first()
    
    if existing_record:
        # Actualizar registro existente
        existing_record.resultado = resultado_enum
        db.commit()
        db.refresh(existing_record)
        return {
            "message": "Ticket actualizado",
            "record": {
                "id": existing_record.id,
                "student_id": existing_record.estudiante_id,
                "unidad": existing_record.unidad,
                "modulo": existing_record.modulo,
                "resultado": existing_record.resultado.value
            }
        }
    else:
        # Crear nuevo registro
        new_record = TicketEstudiante(
            estudiante_id=request.student_id,
            unidad=request.unidad,
            modulo=request.modulo,
            resultado=resultado_enum
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return {
            "message": "Ticket creado",
            "record": {
                "id": new_record.id,
                "student_id": new_record.estudiante_id,
                "unidad": new_record.unidad,
                "modulo": new_record.modulo,
                "resultado": new_record.resultado.value
            }
        }
