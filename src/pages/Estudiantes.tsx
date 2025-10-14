import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface School {
  id: number;
  name: string;
  comuna: string;
}

interface Student {
  id: number;
  rut: string;
  first_name: string;
  last_name: string;
  course: string;
  school_id: number;
  guardian_name?: string;
  guardian_contact?: string;
  observations?: string;
  attendance_percentage: number;
  school: School;
  created_at: string;
  updated_at?: string;
}

const Estudiantes: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token } = useAuth();

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await fetch('http://localhost:8000/students/', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Estudiantes recibidos:', data);
          setStudents(data);
        } else {
          setError('Error al cargar los estudiantes');
        }
      } catch (err) {
        setError('Error de conexión');
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchStudents();
    }
  }, [token]);

  const getAttendanceColor = (percentage: number) => {
    if (percentage >= 80) return 'attendance-high';
    if (percentage >= 60) return 'attendance-medium';
    return 'attendance-low';
  };

  return (
    <div className="page-container">
      <h1 className="page-title">Estudiantes</h1>
      <p className="page-description">
        Gestiona la información de todos los estudiantes del programa de tutorías. 
        Aquí podrás consultar datos personales, historial académico y estado actual.
      </p>

      <div className="students-section">
        <h2 className="section-title">Lista de Estudiantes</h2>
        
        {loading && (
          <div className="loading">
            <p>Cargando estudiantes...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {!loading && !error && students.length === 0 && (
          <div className="no-data">
            <p>No hay estudiantes registrados</p>
          </div>
        )}

        {!loading && !error && students.length > 0 && (
          <div className="students-table-container">
            <table className="students-table">
              <thead>
                <tr>
                  <th>RUT</th>
                  <th>Nombre Completo</th>
                  <th>Curso</th>
                  <th>Colegio</th>
                  <th>Comuna</th>
                  <th>% Asistencia</th>
                  <th>Apoderado</th>
                  <th>Contacto</th>
                  <th>Observaciones</th>
                  <th>Fecha de Registro</th>
                </tr>
              </thead>
              <tbody>
                {students.map((student) => (
                  <tr key={student.id}>
                    <td className="rut-cell">{student.rut}</td>
                    <td className="name-cell">{student.first_name} {student.last_name}</td>
                    <td>{student.course}</td>
                    <td>{student.school.name}</td>
                    <td>{student.school.comuna}</td>
                    <td className={`attendance-cell ${getAttendanceColor(student.attendance_percentage)}`}>
                      {student.attendance_percentage}%
                    </td>
                    <td>{student.guardian_name || 'N/A'}</td>
                    <td>{student.guardian_contact || 'N/A'}</td>
                    <td className="observations-cell">{student.observations || 'N/A'}</td>
                    <td>{new Date(student.created_at).toLocaleDateString('es-ES')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Estudiantes;
