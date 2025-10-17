import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AttendanceChart from '../components/AttendanceChart';

interface Estudiante {
  id: number;
  nombre: string;
  apellido: string;
  curso: string;
  equipo_id: number;
}

interface Tutor {
  id: number;
  nombre: string;
  apellido: string;
  equipo_id: number;
}

interface Equipo {
  id: number;
  nombre: string;
  descripcion: string;
  colegio_id: number;
  colegio?: {
    id: number;
    nombre: string;
    comuna: string;
  };
}

interface StudentAttendanceData {
  student_id: number;
  student_name: string;
  course: string;
  attendance_percentage: number;
  attended_weeks: number;
  absent_weeks: number;
  total_weeks: number;
}

interface AttendanceStats {
  students_stats: StudentAttendanceData[];
  overall_average: number;
  students_with_3_plus_absences: Array<{
    student_id: number;
    student_name: string;
    course: string;
    absent_weeks: number;
  }>;
  total_students: number;
}

const Dashboard: React.FC = () => {
  const [estudiantes, setEstudiantes] = useState<Estudiante[]>([]);
  const [tutores, setTutores] = useState<Tutor[]>([]);
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [attendanceStats, setAttendanceStats] = useState<AttendanceStats | null>(null);
  const [filteredAttendanceStats, setFilteredAttendanceStats] = useState<AttendanceStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token, user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
        
        // Cargar estudiantes
        const estudiantesResponse = await fetch(`${apiUrl}/estudiantes/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (estudiantesResponse.ok) {
          const estudiantesData = await estudiantesResponse.json();
          setEstudiantes(estudiantesData);
        }

        // Cargar tutores
        const tutoresResponse = await fetch(`${apiUrl}/tutores/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (tutoresResponse.ok) {
          const tutoresData = await tutoresResponse.json();
          setTutores(tutoresData);
        }

        // Cargar equipos (solo si es admin)
        if (user?.rol === 'admin') {
          const equiposResponse = await fetch(`${apiUrl}/equipos/`, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (equiposResponse.ok) {
            const equiposData = await equiposResponse.json();
            setEquipos(equiposData);
          }
        }

        // Cargar estadísticas de asistencia
        const attendanceResponse = await fetch(`${apiUrl}/attendance/students/attendance-stats`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (attendanceResponse.ok) {
          const attendanceData = await attendanceResponse.json();
          setAttendanceStats(attendanceData);
        }

      } catch (err) {
        setError('Error de conexión al cargar datos');
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchData();
    }
  }, [token, user]);

  // Filtrar estadísticas de asistencia por equipo cuando cambien los estudiantes
  useEffect(() => {
    if (attendanceStats && estudiantes.length > 0) {
      if (user?.rol === 'tutor' && user?.equipo_id) {
        // Filtrar solo los estudiantes del equipo del tutor
        const filteredStats = attendanceStats.students_stats.filter((student: any) => {
          const estudiante = estudiantes.find(e => e.id === student.student_id);
          return estudiante && estudiante.equipo_id === user.equipo_id;
        });
        
        const filteredAbsences = attendanceStats.students_with_3_plus_absences.filter((student: any) => {
          const estudiante = estudiantes.find(e => e.id === student.student_id);
          return estudiante && estudiante.equipo_id === user.equipo_id;
        });
        
        // Recalcular promedio solo para el equipo
        const totalAttended = filteredStats.reduce((sum: number, student: any) => sum + student.attended_weeks, 0);
        const totalPossible = filteredStats.reduce((sum: number, student: any) => sum + student.total_weeks, 0);
        const teamAverage = totalPossible > 0 ? (totalAttended / totalPossible) * 100 : 0;
        
        setFilteredAttendanceStats({
          students_stats: filteredStats,
          overall_average: Math.round(teamAverage * 100) / 100,
          students_with_3_plus_absences: filteredAbsences,
          total_students: filteredStats.length
        });
      } else {
        // Si es admin, mostrar todos los datos
        setFilteredAttendanceStats(attendanceStats);
      }
    }
  }, [attendanceStats, estudiantes, user]);

  const getEquipoNombre = (equipoId: number) => {
    const equipo = equipos.find(e => e.id === equipoId);
    return equipo ? equipo.nombre : `Equipo ${equipoId}`;
  };

  const getColegioNombre = (equipoId: number) => {
    const equipo = equipos.find(e => e.id === equipoId);
    return equipo?.colegio?.nombre || 'Sin colegio';
  };

  return (
    <div className="page-container">
      <h1 className="page-title">Dashboard</h1>

      {loading && (
        <div className="loading">
          <p>Cargando datos...</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && (
        <>
          {/* Estadísticas generales - más compactas */}
          <div className="stats-section">
            <div className="stats-grid-horizontal">
              <div className="stat-card-compact">
                <h3>Estudiantes</h3>
                <p className="stat-number">{estudiantes.length}</p>
                {user?.rol === 'tutor' && (
                  <p className="stat-detail">en tu equipo</p>
                )}
              </div>
              
              <div className="stat-card-compact">
                <h3>Tutores</h3>
                <p className="stat-number">{tutores.length}</p>
                {user?.rol === 'tutor' && (
                  <p className="stat-detail">en tu equipo</p>
                )}
              </div>

              {user?.rol === 'admin' && (
                <div className="stat-card-compact">
                  <h3>Equipos</h3>
                  <p className="stat-number">{equipos.length}</p>
                </div>
              )}
            </div>
          </div>

          {/* Estadísticas de Asistencia - más compactas */}
          {filteredAttendanceStats && (
            <>
              {/* Promedio de Asistencia - 2 cuadritos pequeños */}
              <div className="attendance-stats-compact">
                <div className="attendance-card-small">
                  <h3>Promedio % Asistencia</h3>
                  <p className="stat-number-small">
                    {filteredAttendanceStats.overall_average}%
                  </p>
                  <p className="stat-detail-small">
                    {filteredAttendanceStats.total_students} estudiantes
                  </p>
                </div>
                
                <div className="warning-card-small">
                  <h3>+3 Inasistencias</h3>
                  <p className="stat-number-small">
                    {filteredAttendanceStats.students_with_3_plus_absences.length}
                  </p>
                  <p className="stat-detail-small">requieren atención</p>
                </div>
              </div>

              {/* Gráfico de Asistencia */}
              <div className="attendance-chart-section">
                <h2 className="section-title">Gráfico de Asistencia por Estudiante</h2>
                <div className="chart-container">
                  <AttendanceChart data={filteredAttendanceStats.students_stats} />
                </div>
              </div>

              {/* Lista de Estudiantes con muchas inasistencias */}
              {filteredAttendanceStats.students_with_3_plus_absences.length > 0 && (
                <div className="students-absences-section">
                  <h2 className="section-title">Estudiantes con más de 3 Inasistencias</h2>
                  <div className="absences-list">
                    {filteredAttendanceStats.students_with_3_plus_absences.map((student) => (
                      <div key={student.student_id} className="absence-card">
                        <h4>{student.student_name}</h4>
                        <p>Curso: {student.course}</p>
                        <p className="absence-count">
                          Inasistencias: {student.absent_weeks}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {/* Tabla de estudiantes */}
          <div className="students-section">
            <h2 className="section-title">Estudiantes</h2>
            {estudiantes.length > 0 ? (
              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Curso</th>
                      <th>Equipo</th>
                      <th>Colegio</th>
                    </tr>
                  </thead>
                  <tbody>
                    {estudiantes.map((estudiante) => (
                      <tr key={estudiante.id}>
                        <td>{estudiante.nombre} {estudiante.apellido}</td>
                        <td>{estudiante.curso}</td>
                        <td>{getEquipoNombre(estudiante.equipo_id)}</td>
                        <td>{getColegioNombre(estudiante.equipo_id)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p>No hay estudiantes disponibles</p>
            )}
          </div>

          {/* Tabla de tutores (solo para admin) */}
          {user?.rol === 'admin' && (
            <div className="tutors-section">
              <h2 className="section-title">Tutores</h2>
              {tutores.length > 0 ? (
                <div className="table-container">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Nombre</th>
                        <th>Equipo</th>
                        <th>Colegio</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tutores.map((tutor) => (
                        <tr key={tutor.id}>
                          <td>{tutor.nombre} {tutor.apellido}</td>
                          <td>{getEquipoNombre(tutor.equipo_id)}</td>
                          <td>{getColegioNombre(tutor.equipo_id)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p>No hay tutores disponibles</p>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Dashboard;
