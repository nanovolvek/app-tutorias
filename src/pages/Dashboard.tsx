import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface School {
  id: number;
  name: string;
  comuna: string;
}

interface Student {
  id: number;
  first_name: string;
  last_name: string;
  course: string;
  school_id: number;
  school?: School;
  created_at: string;
  updated_at?: string;
}

const Dashboard: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token } = useAuth();

  // Mapeo de colegios (temporal hasta que el endpoint funcione correctamente)
  const schoolsMap: { [key: number]: { name: string; comuna: string } } = {
    1: { name: 'Colegio San Patricio', comuna: 'Las Condes' },
    2: { name: 'Liceo Manuel Barros Borgoño', comuna: 'Santiago' }
  };

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

  return (
    <div className="page-container">
      <h1 className="page-title">Dashboard</h1>
      <p className="page-description">
        Bienvenido a la Plataforma de Tutorías. Aquí podrás ver un resumen general 
        del programa, estadísticas de asistencia, y acceso rápido a las funciones principales.
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
                  <th>ID</th>
                  <th>Nombre Completo</th>
                  <th>Curso</th>
                  <th>Colegio</th>
                  <th>Comuna</th>
                  <th>Fecha de Registro</th>
                </tr>
              </thead>
              <tbody>
                {students.map((student) => {
                  const schoolInfo = schoolsMap[student.school_id];
                  return (
                    <tr key={student.id}>
                      <td>{student.id}</td>
                      <td>{student.first_name} {student.last_name}</td>
                      <td>{student.course}</td>
                      <td>{schoolInfo?.name || 'N/A'}</td>
                      <td>{schoolInfo?.comuna || 'N/A'}</td>
                      <td>{new Date(student.created_at).toLocaleDateString('es-ES')}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
