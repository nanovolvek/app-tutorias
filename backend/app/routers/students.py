from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.student import Student
from app.models.school import School
from app.schemas.student import Student as StudentSchema, StudentCreate, StudentUpdate, StudentWithSchool, StudentWithAttendance
from app.models.attendance import Attendance
from app.auth.dependencies import get_current_active_user, get_admin_user
from app.models.user import User

router = APIRouter(prefix="/students", tags=["estudiantes"])

@router.get("/", response_model=List[StudentWithAttendance])
def get_students(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener lista de estudiantes con información del colegio y porcentaje de asistencia"""
    # Hacer una consulta manual que incluya la información del colegio
    result = db.query(Student, School).join(School, Student.school_id == School.id).offset(skip).limit(limit).all()
    
    # Construir la respuesta con la información del colegio y asistencia
    students_with_school = []
    for student, school in result:
        # Calcular porcentaje de asistencia
        attendance_records = db.query(Attendance).filter(Attendance.student_id == student.id).all()
        attended_weeks = sum(1 for record in attendance_records if record.attended)
        total_weeks = 10
        attendance_percentage = (attended_weeks / total_weeks) * 100 if total_weeks > 0 else 0
        
        student_dict = {
            "id": student.id,
            "rut": student.rut,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "course": student.course,
            "school_id": student.school_id,
            "guardian_name": student.guardian_name,
            "guardian_contact": student.guardian_contact,
            "observations": student.observations,
            "created_at": student.created_at,
            "updated_at": student.updated_at,
            "attendance_percentage": round(attendance_percentage, 2),
            "school": {
                "id": school.id,
                "name": school.name,
                "comuna": school.comuna
            }
        }
        students_with_school.append(student_dict)
    
    return students_with_school

@router.get("/{student_id}", response_model=StudentSchema)
def get_student(
    student_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un estudiante por ID"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return student

@router.post("/", response_model=StudentSchema)
def create_student(
    student: StudentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Crear un nuevo estudiante (solo administradores)"""
    # Verificar que el colegio existe
    school = db.query(School).filter(School.id == student.school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.put("/{student_id}", response_model=StudentSchema)
def update_student(
    student_id: int, 
    student: StudentUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Actualizar un estudiante (solo administradores)"""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Si se actualiza el school_id, verificar que existe
    if student.school_id is not None:
        school = db.query(School).filter(School.id == student.school_id).first()
        if school is None:
            raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    update_data = student.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/{student_id}")
def delete_student(
    student_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Eliminar un estudiante (solo administradores)"""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    db.delete(db_student)
    db.commit()
    return {"message": "Estudiante eliminado correctamente"}
