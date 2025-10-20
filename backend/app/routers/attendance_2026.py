from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.attendance import AsistenciaEstudiante, AsistenciaTutor, EstadoAsistencia
from app.models.student import Estudiante
from app.models.tutor import Tutor
from app.models.school import Colegio
from app.models.equipo import Equipo
from app.schemas.attendance import AttendanceStatus
from app.auth.dependencies import get_current_user
from pydantic import BaseModel
import json
import os

router = APIRouter(prefix="/attendance-2026", tags=["attendance-2026"])

class AttendanceUpdateRequest(BaseModel):
    student_id: Optional[int] = None
    tutor_id: Optional[int] = None
    week_key: str
    status: str

# Cargar calendario 2026
def load_2026_calendar():
    """Cargar el calendario 2026 desde archivo JSON"""
    calendar_path = os.path.join(os.path.dirname(__file__), "..", "..", "calendar_2026.json")
    try:
        with open(calendar_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Si no existe el archivo, generar calendario básico
        return generate_basic_calendar()

def generate_basic_calendar():
    """Generar calendario básico si no existe el archivo"""
    months = {
        "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6, 
        "Julio": 7, "Agosto": 8, "Septiembre": 9, 
        "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }
    
    weeks = []
    week_num = 1
    
    # Generar semanas básicas para cada mes
    for month_name, month_num in months.items():
        for week_in_month in range(1, 5):  # 4 semanas por mes aproximadamente
            if week_num <= 43:  # Solo 43 semanas
                weeks.append({
                    "semana_numero": week_num,
                    "semana_key": f"semana_{week_num}",
                    "mes": month_name,
                    "dias": f"{week_in_month*7-6} al {week_in_month*7}",
                    "fecha_inicio": f"2026-{month_num:02d}-{week_in_month*7-6:02d}",
                    "fecha_fin": f"2026-{month_num:02d}-{week_in_month*7:02d}",
                    "mes_numero": month_num
                })
                week_num += 1
    
    return weeks

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

@router.get("/calendar/weeks")
def get_calendar_weeks():
    """Obtener el calendario completo de 2026 con todas las semanas"""
    calendar = load_2026_calendar()
    return {"weeks": calendar, "total_weeks": len(calendar)}

@router.get("/students")
def get_students_attendance(
    month: Optional[str] = Query(None, description="Mes para filtrar (ej: Marzo, Abril)"),
    school_id: Optional[int] = Query(None, description="ID del colegio"),
    equipo_id: Optional[int] = Query(None, description="ID del equipo"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener estudiantes con sus registros de asistencia filtrados por mes, colegio y equipo"""
    
    try:
        # Construir query base
        query = db.query(Estudiante)
        
        # Aplicar filtros
        if school_id:
            query = query.join(Equipo).join(Colegio).filter(Colegio.id == school_id)
        
        if equipo_id:
            query = query.filter(Estudiante.equipo_id == equipo_id)
        
        estudiantes = query.all()
        
        # Obtener semanas del mes si se especifica
        calendar = load_2026_calendar()
        month_weeks = []
        if month:
            month_weeks = [week for week in calendar if week["mes"] == month]
        
        result = []
        
        for estudiante in estudiantes:
            # Obtener registros de asistencia del estudiante
            attendance_query = db.query(AsistenciaEstudiante).filter(
                AsistenciaEstudiante.estudiante_id == estudiante.id
            )
            
            if month_weeks:
                week_keys = [week["semana_key"] for week in month_weeks]
                attendance_query = attendance_query.filter(
                    AsistenciaEstudiante.semana.in_(week_keys)
                )
            
            attendance_records = attendance_query.all()
            
            # Crear diccionario de asistencia
            weekly_attendance = {}
            for record in attendance_records:
                if record.estado:  # Verificar que estado no sea None
                    weekly_attendance[record.semana] = record.estado.value
            
            result.append({
                "id": estudiante.id,
                "nombre": estudiante.nombre,
                "apellido": estudiante.apellido,
                "curso": estudiante.curso,
                "colegio_id": estudiante.equipo.colegio_id if estudiante.equipo else None,
                "equipo_id": estudiante.equipo_id,
                "colegio_nombre": estudiante.equipo.colegio.nombre if estudiante.equipo and estudiante.equipo.colegio else "Sin colegio",
                "equipo_nombre": estudiante.equipo.nombre if estudiante.equipo else "Sin equipo",
                "weekly_attendance": weekly_attendance
            })
        
        return {
            "students": result,
            "total_students": len(result),
            "month": month,
            "school_id": school_id,
            "equipo_id": equipo_id
        }
    except Exception as e:
        print(f"Error en get_students_attendance: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/tutors")
def get_tutors_attendance(
    month: Optional[str] = Query(None, description="Mes para filtrar (ej: Marzo, Abril)"),
    school_id: Optional[int] = Query(None, description="ID del colegio"),
    equipo_id: Optional[int] = Query(None, description="ID del equipo"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener tutores con sus registros de asistencia filtrados por mes, colegio y equipo"""
    
    # Construir query base
    query = db.query(Tutor)
    
    # Aplicar filtros
    if school_id:
        query = query.join(Equipo).join(Colegio).filter(Colegio.id == school_id)
    
    if equipo_id:
        query = query.filter(Tutor.equipo_id == equipo_id)
    
    tutores = query.all()
    
    # Obtener semanas del mes si se especifica
    calendar = load_2026_calendar()
    month_weeks = []
    if month:
        month_weeks = [week for week in calendar if week["mes"] == month]
    
    result = []
    
    for tutor in tutores:
        # Obtener registros de asistencia del tutor
        attendance_query = db.query(AsistenciaTutor).filter(
            AsistenciaTutor.tutor_id == tutor.id
        )
        
        if month_weeks:
            week_keys = [week["semana_key"] for week in month_weeks]
            attendance_query = attendance_query.filter(
                AsistenciaTutor.semana.in_(week_keys)
            )
        
        attendance_records = attendance_query.all()
        
        # Crear diccionario de asistencia
        weekly_attendance = {}
        for record in attendance_records:
            if record.estado:  # Verificar que estado no sea None
                weekly_attendance[record.semana] = record.estado.value
        
        result.append({
            "id": tutor.id,
            "nombre": tutor.nombre,
            "apellido": tutor.apellido,
            "email": tutor.email,
            "colegio_id": tutor.equipo.colegio_id if tutor.equipo else None,
            "equipo_id": tutor.equipo_id,
            "colegio_nombre": tutor.equipo.colegio.nombre if tutor.equipo and tutor.equipo.colegio else "Sin colegio",
            "equipo_nombre": tutor.equipo.nombre if tutor.equipo else "Sin equipo",
            "weekly_attendance": weekly_attendance
        })
    
    return {
        "tutors": result,
        "total_tutors": len(result),
        "month": month,
        "school_id": school_id,
        "equipo_id": equipo_id
    }

@router.post("/students")
def update_student_attendance(
    request: AttendanceUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear o actualizar registro de asistencia de estudiante"""
    
    # Verificar que el estudiante existe
    student = db.query(Estudiante).filter(Estudiante.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Verificar que el estado es válido
    try:
        estado_enum = EstadoAsistencia(request.status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Estado de asistencia inválido")
    
    # Buscar registro existente
    existing_record = db.query(AsistenciaEstudiante).filter(
        AsistenciaEstudiante.estudiante_id == request.student_id,
        AsistenciaEstudiante.semana == request.week_key
    ).first()
    
    if existing_record:
        # Actualizar registro existente
        existing_record.estado = estado_enum
        db.commit()
        db.refresh(existing_record)
        return {
            "message": "Registro de asistencia actualizado",
            "record": {
                "id": existing_record.id,
                "student_id": existing_record.estudiante_id,
                "week": existing_record.semana,
                "status": existing_record.estado.value
            }
        }
    else:
        # Crear nuevo registro
        new_record = AsistenciaEstudiante(
            estudiante_id=request.student_id,
            semana=request.week_key,
            estado=estado_enum
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return {
            "message": "Registro de asistencia creado",
            "record": {
                "id": new_record.id,
                "student_id": new_record.estudiante_id,
                "week": new_record.semana,
                "status": new_record.estado.value
            }
        }

@router.post("/tutors")
def update_tutor_attendance(
    request: AttendanceUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear o actualizar registro de asistencia de tutor"""
    
    # Verificar que el tutor existe
    tutor = db.query(Tutor).filter(Tutor.id == request.tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    # Verificar que el estado es válido
    try:
        estado_enum = EstadoAsistencia(request.status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Estado de asistencia inválido")
    
    # Buscar registro existente
    existing_record = db.query(AsistenciaTutor).filter(
        AsistenciaTutor.tutor_id == request.tutor_id,
        AsistenciaTutor.semana == request.week_key
    ).first()
    
    if existing_record:
        # Actualizar registro existente
        existing_record.estado = estado_enum
        db.commit()
        db.refresh(existing_record)
        return {
            "message": "Registro de asistencia actualizado",
            "record": {
                "id": existing_record.id,
                "tutor_id": existing_record.tutor_id,
                "week": existing_record.semana,
                "status": existing_record.estado.value
            }
        }
    else:
        # Crear nuevo registro
        new_record = AsistenciaTutor(
            tutor_id=request.tutor_id,
            semana=request.week_key,
            estado=estado_enum
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return {
            "message": "Registro de asistencia creado",
            "record": {
                "id": new_record.id,
                "tutor_id": new_record.tutor_id,
                "week": new_record.semana,
                "status": new_record.estado.value
            }
        }
