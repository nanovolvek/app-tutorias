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

# Datos de módulos por unidad con nombres reales
# Nota: Los modulo_key se mantienen como modulo_1, modulo_2, etc. para cada unidad
# para mantener compatibilidad con datos existentes en la base de datos
MODULOS_DATA = {
    "unidad_1": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 1", "descripcion": "Adicción de N° Naturales"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 2", "descripcion": "Sustracción de N° Naturales"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 3", "descripcion": "Multiplicación de N° Naturales"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 4", "descripcion": "División de N° Naturales"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 5", "descripcion": "Operatoria Combinada de N° Naturales"}
    ],
    "unidad_2": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 6", "descripcion": "Adicción de N° Enteros"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 7", "descripcion": "Sustracción de N° Enteros"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 8", "descripcion": "Multiplicación y división de N° Enteros"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 9", "descripcion": "Operatoria Combinada de N° Enteros"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 10", "descripcion": "Resolución de Problemas de N° Enteros"}
    ],
    "unidad_3": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 11", "descripcion": "Conceptos Claves de Fracciones"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 12", "descripcion": "Suma y Resta de Fracciones"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 13", "descripcion": "Multiplicación de Fracciones"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 14", "descripcion": "División de Fracciones"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 15", "descripcion": "Suma y Resta de Decimales"},
        {"modulo_key": "modulo_6", "nombre": "Módulo 16", "descripcion": "Multiplicación de Decimales"},
        {"modulo_key": "modulo_7", "nombre": "Módulo 17", "descripcion": "División de Decimales"},
        {"modulo_key": "modulo_8", "nombre": "Módulo 18", "descripcion": "Conjuntos Numéricos"},
        {"modulo_key": "modulo_9", "nombre": "Módulo 19", "descripcion": "Operatoria Combinada de N° Racionales"},
        {"modulo_key": "modulo_10", "nombre": "Módulo 20", "descripcion": "Resolución de Problemas de N° Racionales"}
    ],
    "unidad_4": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 21", "descripcion": "Conceptos Claves de %"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 22", "descripcion": "Cálculo de % más directos"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 23", "descripcion": "Cálculo de cualquier %"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 24", "descripcion": "Resolución de Problemas de % 1"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 25", "descripcion": "Resolución de Problemas de % 2"}
    ],
    "unidad_5": [
        {"modulo_key": "modulo_1", "nombre": "Módulo 26", "descripcion": "Conceptos Claves de Raíces"},
        {"modulo_key": "modulo_2", "nombre": "Módulo 27", "descripcion": "Cálculo de Raíces"},
        {"modulo_key": "modulo_3", "nombre": "Módulo 28", "descripcion": "Propiedades de Raíces"},
        {"modulo_key": "modulo_4", "nombre": "Módulo 29", "descripcion": "Resolución de Problemas de Raíces"},
        {"modulo_key": "modulo_5", "nombre": "Módulo 30", "descripcion": "Conceptos Claves de Potencias"},
        {"modulo_key": "modulo_6", "nombre": "Módulo 31", "descripcion": "Cálculo de Potencias"},
        {"modulo_key": "modulo_7", "nombre": "Módulo 32", "descripcion": "Propiedades de Potencias"},
        {"modulo_key": "modulo_8", "nombre": "Módulo 33", "descripcion": "Resolución de Problemas de Potencias"}
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

@router.get("/export-all")
def get_all_tickets_for_export(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener todos los tickets para exportación a Excel (respetando roles)"""
    try:
        # Construir query base de estudiantes
        query = db.query(Estudiante).join(Equipo).join(Colegio)
        
        # Aplicar filtros según el rol del usuario
        if current_user.rol == 'tutor':
            # Tutor solo ve estudiantes de su equipo
            query = query.filter(Estudiante.equipo_id == current_user.equipo_id)
        
        estudiantes = query.all()
        
        # Obtener todos los tickets de todos los estudiantes
        all_tickets_data = []
        
        # Crear un mapa de tickets existentes por estudiante
        tickets_map = {}
        all_tickets = db.query(TicketEstudiante).all()
        for ticket in all_tickets:
            if ticket.estudiante_id not in tickets_map:
                tickets_map[ticket.estudiante_id] = []
            tickets_map[ticket.estudiante_id].append(ticket)
        
        # Para cada estudiante, generar entradas para todas las unidades y módulos
        for estudiante in estudiantes:
            estudiante_tickets = tickets_map.get(estudiante.id, [])
            tickets_dict = {(t.unidad, t.modulo): t for t in estudiante_tickets}
            
            # Generar todas las combinaciones de unidad y módulo
            for unidad_key, modulos in MODULOS_DATA.items():
                unidad_nombre = f"Unidad {unidad_key.split('_')[1]}"
                for modulo in modulos:
                    ticket_key = (unidad_key, modulo["modulo_key"])
                    ticket = tickets_dict.get(ticket_key)
                    
                    all_tickets_data.append({
                        "estudiante_id": estudiante.id,
                        "rut": estudiante.rut,
                        "nombre": estudiante.nombre,
                        "apellido": estudiante.apellido,
                        "curso": estudiante.curso,
                        "equipo_id": estudiante.equipo_id,
                        "equipo_nombre": estudiante.equipo.nombre if estudiante.equipo else "Sin equipo",
                        "colegio_id": estudiante.equipo.colegio_id if estudiante.equipo else None,
                        "colegio_nombre": estudiante.equipo.colegio.nombre if estudiante.equipo and estudiante.equipo.colegio else "Sin colegio",
                        "unidad": unidad_key,
                        "unidad_nombre": unidad_nombre,
                        "modulo": modulo["modulo_key"],
                        "modulo_nombre": modulo["nombre"],
                        "resultado": ticket.resultado.value if ticket and ticket.resultado else "vacío",
                        "created_at": ticket.created_at.isoformat() if ticket and ticket.created_at else None,
                        "updated_at": ticket.updated_at.isoformat() if ticket and ticket.updated_at else None
                    })
        
        return {
            "tickets": all_tickets_data,
            "total": len(all_tickets_data)
        }
        
    except Exception as e:
        print(f"Error en get_all_tickets_for_export: {e}")
        import traceback
        traceback.print_exc()
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
