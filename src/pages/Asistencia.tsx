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

interface AttendanceRecord {
  id: number;
  student_id?: number;
  tutor_id?: number;
  week: string;
  status: 'asistió' | 'no asistió' | 'tutoría suspendida' | 'vacaciones/feriado';
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

      <style jsx>{`
        .attendance-tabs {
          display: flex;
          gap: 1rem;
          margin-bottom: 2rem;
        }

        .tab-button {
          padding: 0.75rem 1.5rem;
          border: 2px solid #e5e7eb;
          background: white;
          border-radius: 0.5rem;
          cursor: pointer;
          font-weight: 500;
          transition: all 0.2s;
        }

        .tab-button:hover {
          border-color: #3b82f6;
          background: #f8fafc;
        }

        .tab-button.active {
          border-color: #3b82f6;
          background: #3b82f6;
          color: white;
        }

        .attendance-form-container {
          background: white;
          padding: 2rem;
          border-radius: 0.75rem;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          max-width: 600px;
        }

        .attendance-form {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .form-group label {
          font-weight: 500;
          color: #374151;
        }

        .form-select {
          padding: 0.75rem;
          border: 1px solid #d1d5db;
          border-radius: 0.5rem;
          font-size: 1rem;
          background: white;
        }

        .form-select:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .submit-button {
          padding: 0.75rem 1.5rem;
          background: #3b82f6;
          color: white;
          border: none;
          border-radius: 0.5rem;
          font-size: 1rem;
          font-weight: 500;
          cursor: pointer;
          transition: background 0.2s;
        }

        .submit-button:hover:not(:disabled) {
          background: #2563eb;
        }

        .submit-button:disabled {
          background: #9ca3af;
          cursor: not-allowed;
        }

        .message {
          margin-top: 1rem;
          padding: 0.75rem;
          border-radius: 0.5rem;
          font-weight: 500;
        }

        .message.success {
          background: #d1fae5;
          color: #065f46;
          border: 1px solid #a7f3d0;
        }

        .message.error {
          background: #fee2e2;
          color: #991b1b;
          border: 1px solid #fca5a5;
        }
      `}</style>
    </div>
  );
};

export default Asistencia;
