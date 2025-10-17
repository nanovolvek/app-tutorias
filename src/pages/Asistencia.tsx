import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Student {
  id: number;
  first_name: string;
  last_name: string;
  course: string;
  school_name: string;
}

interface Tutor {
  id: number;
  first_name: string;
  last_name: string;
  school_name: string;
}


const Asistencia: React.FC = () => {
  const { token } = useAuth();
  const [activeTab, setActiveTab] = useState<'students' | 'tutors'>('students');
  const [students, setStudents] = useState<Student[]>([]);
  const [tutors, setTutors] = useState<Tutor[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<number | null>(null);
  const [selectedTutor, setSelectedTutor] = useState<number | null>(null);
  const [selectedWeek, setSelectedWeek] = useState<string>('semana_1');
  const [attendanceStatus, setAttendanceStatus] = useState<'asistió' | 'no asistió' | 'tutoría suspendida' | 'vacaciones/feriado'>('no asistió');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const weeks = Array.from({ length: 10 }, (_, i) => `semana_${i + 1}`);

  useEffect(() => {
    fetchStudents();
    fetchTutors();
  }, []);

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
        setStudents(data);
      }
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  };

  const fetchTutors = async () => {
    try {
      const response = await fetch('http://localhost:8000/tutors/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        setTutors(data);
      }
    } catch (error) {
      console.error('Error fetching tutors:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const url = activeTab === 'students' 
        ? 'http://localhost:8000/attendance/student'
        : 'http://localhost:8000/tutor-attendance/';
      
      const body = activeTab === 'students'
        ? {
            student_id: selectedStudent,
            week: selectedWeek,
            status: attendanceStatus
          }
        : {
            tutor_id: selectedTutor,
            week: selectedWeek,
            status: attendanceStatus
          };

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        setMessage('Asistencia registrada correctamente');
        // Reset form
        setSelectedStudent(null);
        setSelectedTutor(null);
        setSelectedWeek('semana_1');
        setAttendanceStatus('no asistió');
      } else {
        const error = await response.json();
        setMessage(`Error: ${error.detail || 'Error al registrar asistencia'}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('Error al conectar con el servidor');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h1 className="page-title">Asistencia</h1>
      <p className="page-description">
        Registra y consulta la asistencia de estudiantes y tutores a las sesiones de tutoría.
      </p>

      {/* Botones de navegación */}
      <div className="attendance-tabs">
        <button
          className={`tab-button ${activeTab === 'students' ? 'active' : ''}`}
          onClick={() => setActiveTab('students')}
        >
          Asistencia Estudiantes
        </button>
        <button
          className={`tab-button ${activeTab === 'tutors' ? 'active' : ''}`}
          onClick={() => setActiveTab('tutors')}
        >
          Asistencia Tutores
        </button>
      </div>

      {/* Formulario de asistencia */}
      <div className="attendance-form-container">
        <form onSubmit={handleSubmit} className="attendance-form">
          <div className="form-group">
            <label htmlFor="person-select">
              {activeTab === 'students' ? 'Seleccionar Estudiante:' : 'Seleccionar Tutor:'}
            </label>
            <select
              id="person-select"
              value={activeTab === 'students' ? selectedStudent || '' : selectedTutor || ''}
              onChange={(e) => {
                const value = parseInt(e.target.value);
                if (activeTab === 'students') {
                  setSelectedStudent(value);
                } else {
                  setSelectedTutor(value);
                }
              }}
              required
              className="form-select"
            >
              <option value="">-- Seleccionar --</option>
              {activeTab === 'students'
                ? students.map((student) => (
                    <option key={student.id} value={student.id}>
                      {student.first_name} {student.last_name} - {student.course} ({student.school_name})
                    </option>
                  ))
                : tutors.map((tutor) => (
                    <option key={tutor.id} value={tutor.id}>
                      {tutor.first_name} {tutor.last_name} ({tutor.school_name})
                    </option>
                  ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="week-select">Semana:</label>
            <select
              id="week-select"
              value={selectedWeek}
              onChange={(e) => setSelectedWeek(e.target.value)}
              required
              className="form-select"
            >
              {weeks.map((week) => (
                <option key={week} value={week}>
                  {week.replace('_', ' ').toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="status-select">Estado de Asistencia:</label>
            <select
              id="status-select"
              value={attendanceStatus}
              onChange={(e) => setAttendanceStatus(e.target.value as any)}
              required
              className="form-select"
            >
              <option value="asistió">Asistió</option>
              <option value="no asistió">No Asistió</option>
              <option value="tutoría suspendida">Tutoría Suspendida</option>
              <option value="vacaciones/feriado">Vacaciones/Feriado</option>
            </select>
          </div>

          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Registrando...' : 'Registrar Asistencia'}
          </button>
        </form>

        {message && (
          <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}
      </div>

    </div>
  );
};

export default Asistencia;
