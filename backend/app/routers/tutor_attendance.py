from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.attendance import AsistenciaTutor, EstadoAsistencia
from app.models.tutor import Tutor
from app.models.school import Colegio
from app.schemas.attendance import (
    TutorAttendanceCreate, 
    TutorAttendanceUpdate, 
    TutorAttendanceSummary,
    AttendanceStatus
)
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/tutor-attendance", tags=["tutor-attendance"])

@router.get("/summary", response_model=List[TutorAttendanceSummary])
def get_tutor_attendance_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtiene el resumen de asistencia de todos los tutores con porcentajes"""
    
    # Obtener todos los tutores con sus equipos y colegios
    tutors = db.query(Tutor).join(Colegio, Tutor.equipo_id == Colegio.id).all()
    
    summary = []
    
    for tutor in tutors:
        # Obtener registros de asistencia del tutor
        attendance_records = db.query(AsistenciaTutor).filter(AsistenciaTutor.tutor_id == tutor.id).all()
        
        # Crear diccionario de asistencia por semana
        weekly_attendance = {}
        attended_weeks = 0
        
        # Inicializar todas las semanas como "no asistió"
        for week_num in range(1, 11):
            week_key = f"semana_{week_num}"
            weekly_attendance[week_key] = "no asistió"
        
        # Marcar las semanas donde el tutor asistió
        for record in attendance_records:
            weekly_attendance[record.semana] = record.estado.value
            if record.estado == EstadoAsistencia.ASISTIO:
                attended_weeks += 1
        
        # Calcular porcentaje de asistencia
        total_weeks = 10
        attendance_percentage = (attended_weeks / total_weeks) * 100 if total_weeks > 0 else 0
        
        summary.append(TutorAttendanceSummary(
            tutor_id=tutor.id,
            tutor_name=f"{tutor.nombre} {tutor.apellido}",
            school_name=tutor.equipo.colegio.nombre if tutor.equipo and tutor.equipo.colegio else "Sin colegio",
            total_weeks=total_weeks,
            attended_weeks=attended_weeks,
            attendance_percentage=round(attendance_percentage, 2),
            weekly_attendance=weekly_attendance
        ))
    
    return summary

@router.post("/", response_model=TutorAttendanceCreate)
def create_tutor_attendance_record(
    attendance: TutorAttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear o actualizar un registro de asistencia de tutor"""
    
    # Verificar que el tutor existe
    tutor = db.query(Tutor).filter(Tutor.id == attendance.tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    # Verificar si ya existe un registro para esta semana
    existing_record = db.query(AsistenciaTutor).filter(
        AsistenciaTutor.tutor_id == attendance.tutor_id,
        AsistenciaTutor.semana == attendance.week
    ).first()
    
    if existing_record:
        # Actualizar registro existente
        existing_record.estado = EstadoAsistencia(attendance.status)
        db.commit()
        db.refresh(existing_record)
        return existing_record
    else:
        # Crear nuevo registro
        db_attendance = AsistenciaTutor(
            tutor_id=attendance.tutor_id,
            semana=attendance.week,
            estado=EstadoAsistencia(attendance.status)
        )
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance

@router.put("/{attendance_id}", response_model=TutorAttendanceCreate)
def update_tutor_attendance_record(
    attendance_id: int,
    attendance_update: TutorAttendanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar un registro de asistencia de tutor existente"""
    
    attendance = db.query(AsistenciaTutor).filter(AsistenciaTutor.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    
    if attendance_update.status is not None:
        attendance.estado = EstadoAsistencia(attendance_update.status)
    
    db.commit()
    db.refresh(attendance)
    return attendance

@router.post("/initialize/{tutor_id}")
def initialize_tutor_attendance(
    tutor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Inicializar registros de asistencia para un tutor (10 semanas)"""
    
    # Verificar que el tutor existe
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    # Crear registros para las 10 semanas
    created_records = []
    for week_num in range(1, 11):
        week_key = f"semana_{week_num}"
        
        # Verificar si ya existe un registro para esta semana
        existing = db.query(AsistenciaTutor).filter(
            AsistenciaTutor.tutor_id == tutor_id,
            AsistenciaTutor.semana == week_key
        ).first()
        
        if not existing:
            attendance_record = AsistenciaTutor(
                tutor_id=tutor_id,
                semana=week_key,
                estado=EstadoAsistencia.NO_ASISTIO  # Por defecto no asistió
            )
            db.add(attendance_record)
            created_records.append(attendance_record)
    
    db.commit()
    
    return {
        "message": f"Se inicializaron {len(created_records)} registros de asistencia para el tutor {tutor_id}",
        "created_records": len(created_records)
    }
