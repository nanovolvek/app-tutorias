import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AttendanceChart from '../components/AttendanceChart';

interface StudentAttendanceSummary {
  student_id: number;
  student_name: string;
  course: string;
  school_name: string;
  total_weeks: number;
  attended_weeks: number;
  attendance_percentage: number;
  weekly_attendance: { [key: string]: boolean };
}

const Dashboard: React.FC = () => {
  const [attendanceData, setAttendanceData] = useState<StudentAttendanceSummary[]>([]);
  const [attendanceLoading, setAttendanceLoading] = useState(true);
  const [attendanceError, setAttendanceError] = useState('');
  const { token } = useAuth();

  useEffect(() => {
    const fetchAttendanceData = async () => {
      try {
        const response = await fetch('http://localhost:8000/attendance/summary', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Datos de asistencia recibidos:', data);
          setAttendanceData(data);
        } else {
          setAttendanceError('Error al cargar los datos de asistencia');
        }
      } catch (err) {
        setAttendanceError('Error de conexión al cargar asistencia');
      } finally {
        setAttendanceLoading(false);
      }
    };

    if (token) {
      fetchAttendanceData();
    }
  }, [token]);

  return (
    <div className="page-container">
      <h1 className="page-title">Dashboard</h1>
      <p className="page-description">
        Bienvenido a la Plataforma de Tutorías. Aquí podrás ver un resumen general 
        del programa, estadísticas de asistencia, y acceso rápido a las funciones principales.
      </p>

      {/* Sección de Gráfico de Asistencia */}
      <div className="attendance-section">
        <h2 className="section-title">Estadísticas de Asistencia</h2>
        
        {attendanceLoading && (
          <div className="loading">
            <p>Cargando datos de asistencia...</p>
          </div>
        )}

        {attendanceError && (
          <div className="error-message">
            <p>{attendanceError}</p>
          </div>
        )}

        {!attendanceLoading && !attendanceError && attendanceData.length > 0 && (
          <AttendanceChart data={attendanceData} />
        )}

        {!attendanceLoading && !attendanceError && attendanceData.length === 0 && (
          <div className="no-data">
            <p>No hay datos de asistencia disponibles</p>
          </div>
        )}
      </div>

    </div>
  );
};

export default Dashboard;
