from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.attendance import AsistenciaEstudiante, AsistenciaTutor, EstadoAsistencia
from app.models.student import Estudiante
from app.models.tutor import Tutor
from app.models.school import Colegio
from app.schemas.attendance import (
    AttendanceCreate, 
    AttendanceUpdate, 
    StudentAttendanceSummary,
    StudentAttendanceCreate,
    StudentAttendanceUpdate,
    StudentAttendance as StudentAttendanceSchema
)
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.get("/summary", response_model=List[StudentAttendanceSummary])
def get_attendance_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtiene el resumen de asistencia de todos los estudiantes con porcentajes"""
    
    # Obtener todos los estudiantes con sus equipos y colegios
    estudiantes = db.query(Estudiante).join(Colegio, Estudiante.equipo_id == Colegio.id).all()
    
    summary = []
    
    for estudiante in estudiantes:
        # Obtener registros de asistencia del estudiante
        attendance_records = db.query(AsistenciaEstudiante).filter(AsistenciaEstudiante.estudiante_id == estudiante.id).all()
        
        # Crear diccionario de asistencia por semana
        weekly_attendance = {}
        attended_weeks = 0
        
        # Inicializar todas las semanas como "no asistió"
        for week_num in range(1, 11):
            week_key = f"semana_{week_num}"
            weekly_attendance[week_key] = "no asistió"
        
        # Marcar las semanas donde el estudiante asistió
        for record in attendance_records:
            weekly_attendance[record.semana] = record.estado.value
            if record.estado == EstadoAsistencia.ASISTIO:
                attended_weeks += 1
        
        # Calcular porcentaje de asistencia
        total_weeks = 10
        attendance_percentage = (attended_weeks / total_weeks) * 100 if total_weeks > 0 else 0
        
        summary.append(StudentAttendanceSummary(
            student_id=estudiante.id,
            student_name=f"{estudiante.nombre} {estudiante.apellido}",
            course=estudiante.curso,
            school_name=estudiante.equipo.nombre if estudiante.equipo else "Sin equipo",
            total_weeks=total_weeks,
            attended_weeks=attended_weeks,
            attendance_percentage=round(attendance_percentage, 2),
            weekly_attendance=weekly_attendance
        ))
    
    return summary

@router.get("/students/attendance-stats")
def get_students_attendance_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtiene estadísticas de asistencia de estudiantes para el dashboard"""
    
    # Obtener todos los estudiantes
    estudiantes = db.query(Estudiante).all()
    
    stats = []
    total_attended = 0
    total_possible = 0
    students_with_3_plus_absences = []
    
    for estudiante in estudiantes:
        # Obtener registros de asistencia del estudiante
        attendance_records = db.query(AsistenciaEstudiante).filter(
            AsistenciaEstudiante.estudiante_id == estudiante.id
        ).all()
        
        attended_weeks = 0
        absent_weeks = 0
        
        for record in attendance_records:
            if record.estado == EstadoAsistencia.ASISTIO:
                attended_weeks += 1
            elif record.estado == EstadoAsistencia.NO_ASISTIO:
                absent_weeks += 1
        
        # Calcular porcentaje de asistencia
        total_weeks = len(attendance_records) if attendance_records else 10
        attendance_percentage = (attended_weeks / total_weeks) * 100 if total_weeks > 0 else 0
        
        stats.append({
            "student_id": estudiante.id,
            "student_name": f"{estudiante.nombre} {estudiante.apellido}",
            "course": estudiante.curso,
            "attendance_percentage": round(attendance_percentage, 2),
            "attended_weeks": attended_weeks,
            "absent_weeks": absent_weeks,
            "total_weeks": total_weeks
        })
        
        total_attended += attended_weeks
        total_possible += total_weeks
        
        # Verificar si tiene más de 3 inasistencias
        if absent_weeks > 3:
            students_with_3_plus_absences.append({
                "student_id": estudiante.id,
                "student_name": f"{estudiante.nombre} {estudiante.apellido}",
                "course": estudiante.curso,
                "absent_weeks": absent_weeks
            })
    
    # Calcular promedio general
    overall_average = (total_attended / total_possible) * 100 if total_possible > 0 else 0
    
    return {
        "students_stats": stats,
        "overall_average": round(overall_average, 2),
        "students_with_3_plus_absences": students_with_3_plus_absences,
        "total_students": len(estudiantes)
    }

@router.get("/tutors/attendance-stats")
def get_tutors_attendance_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtiene estadísticas de asistencia de tutores para el dashboard"""
    
    # Obtener todos los tutores
    tutores = db.query(Tutor).all()
    
    stats = []
    total_attended = 0
    total_possible = 0
    tutors_with_3_plus_absences = []
    
    for tutor in tutores:
        # Obtener registros de asistencia del tutor
        attendance_records = db.query(AsistenciaTutor).filter(
            AsistenciaTutor.tutor_id == tutor.id
        ).all()
        
        attended_weeks = 0
        absent_weeks = 0
        
        for record in attendance_records:
            if record.estado == EstadoAsistencia.ASISTIO:
                attended_weeks += 1
            elif record.estado == EstadoAsistencia.NO_ASISTIO:
                absent_weeks += 1
        
        # Calcular porcentaje de asistencia
        total_weeks = len(attendance_records) if attendance_records else 10
        attendance_percentage = (attended_weeks / total_weeks) * 100 if total_weeks > 0 else 0
        
        stats.append({
            "tutor_id": tutor.id,
            "tutor_name": f"{tutor.nombre} {tutor.apellido}",
            "attendance_percentage": round(attendance_percentage, 2),
            "attended_weeks": attended_weeks,
            "absent_weeks": absent_weeks,
            "total_weeks": total_weeks
        })
        
        total_attended += attended_weeks
        total_possible += total_weeks
        
        # Verificar si tiene más de 3 inasistencias
        if absent_weeks > 3:
            tutors_with_3_plus_absences.append({
                "tutor_id": tutor.id,
                "tutor_name": f"{tutor.nombre} {tutor.apellido}",
                "absent_weeks": absent_weeks
            })
    
    # Calcular promedio general
    overall_average = (total_attended / total_possible) * 100 if total_possible > 0 else 0
    
    return {
        "tutors_stats": stats,
        "overall_average": round(overall_average, 2),
        "tutors_with_3_plus_absences": tutors_with_3_plus_absences,
        "total_tutors": len(tutores)
    }

@router.post("/", response_model=AttendanceCreate)
def create_attendance_record(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear o actualizar un registro de asistencia"""
    
    # Verificar que el estudiante existe
    student = db.query(Student).filter(Student.id == attendance.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Verificar si ya existe un registro para esta semana
    existing_record = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.week == attendance.week
    ).first()
    
    if existing_record:
        # Actualizar registro existente
        existing_record.attended = attendance.attended
        db.commit()
        db.refresh(existing_record)
        return existing_record
    else:
        # Crear nuevo registro
        db_attendance = Attendance(**attendance.dict())
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance

@router.put("/{attendance_id}", response_model=AttendanceCreate)
def update_attendance_record(
    attendance_id: int,
    attendance_update: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar un registro de asistencia existente"""
    
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    
    if attendance_update.attended is not None:
        attendance.attended = attendance_update.attended
    
    db.commit()
    db.refresh(attendance)
    return attendance

@router.post("/initialize/{student_id}")
def initialize_student_attendance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Inicializar registros de asistencia para un estudiante (10 semanas)"""
    
    # Verificar que el estudiante existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Crear registros para las 10 semanas
    created_records = []
    for week_num in range(1, 11):
        week_key = f"semana_{week_num}"
        
        # Verificar si ya existe un registro para esta semana
        existing = db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.week == week_key
        ).first()
        
        if not existing:
            attendance_record = Attendance(
                student_id=student_id,
                week=week_key,
                attended=False  # Por defecto no asistió
            )
            db.add(attendance_record)
            created_records.append(attendance_record)
    
    db.commit()
    
    return {
        "message": f"Se inicializaron {len(created_records)} registros de asistencia para el estudiante {student_id}",
        "created_records": len(created_records)
    }

# Nuevas rutas para el modelo mejorado de asistencia de estudiantes
@router.post("/student", response_model=StudentAttendanceSchema)
def create_student_attendance_record(
    attendance: StudentAttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear o actualizar un registro de asistencia de estudiante"""
    
    # Verificar que el estudiante existe
    student = db.query(Student).filter(Student.id == attendance.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Verificar si ya existe un registro para esta semana
    existing_record = db.query(StudentAttendance).filter(
        StudentAttendance.student_id == attendance.student_id,
        StudentAttendance.week == attendance.week
    ).first()
    
    if existing_record:
        # Actualizar registro existente
        existing_record.status = attendance.status
        db.commit()
        db.refresh(existing_record)
        return existing_record
    else:
        # Crear nuevo registro
        db_attendance = StudentAttendance(**attendance.dict())
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance

@router.put("/student/{attendance_id}", response_model=StudentAttendanceSchema)
def update_student_attendance_record(
    attendance_id: int,
    attendance_update: StudentAttendanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar un registro de asistencia de estudiante existente"""
    
    attendance = db.query(StudentAttendance).filter(StudentAttendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    
    if attendance_update.status is not None:
        attendance.status = attendance_update.status
    
    db.commit()
    db.refresh(attendance)
    return attendance

@router.post("/student/initialize/{student_id}")
def initialize_student_attendance_new(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Inicializar registros de asistencia para un estudiante (10 semanas) con el nuevo modelo"""
    
    # Verificar que el estudiante existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Crear registros para las 10 semanas
    created_records = []
    for week_num in range(1, 11):
        week_key = f"semana_{week_num}"
        
        # Verificar si ya existe un registro para esta semana
        existing = db.query(StudentAttendance).filter(
            StudentAttendance.student_id == student_id,
            StudentAttendance.week == week_key
        ).first()
        
        if not existing:
            attendance_record = StudentAttendance(
                student_id=student_id,
                week=week_key,
                status=AttendanceStatus.NOT_ATTENDED  # Por defecto no asistió
            )
            db.add(attendance_record)
            created_records.append(attendance_record)
    
    db.commit()
    
    return {
        "message": f"Se inicializaron {len(created_records)} registros de asistencia para el estudiante {student_id}",
        "created_records": len(created_records)
    }
