import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AttendanceChart from '../components/AttendanceChart';
import CreateSchoolTeamForm from '../components/CreateSchoolTeamForm';

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

interface TutorAttendanceData {
  tutor_id: number;
  tutor_name: string;
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

interface TutorAttendanceStats {
  tutors_stats: TutorAttendanceData[];
  overall_average: number;
  tutors_with_3_plus_absences: Array<{
    tutor_id: number;
    tutor_name: string;
    absent_weeks: number;
  }>;
  total_tutors: number;
}

const Dashboard: React.FC = () => {
  const [estudiantes, setEstudiantes] = useState<Estudiante[]>([]);
  const [tutores, setTutores] = useState<Tutor[]>([]);
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [attendanceStats, setAttendanceStats] = useState<AttendanceStats | null>(null);
  const [tutorAttendanceStats, setTutorAttendanceStats] = useState<TutorAttendanceStats | null>(null);
  const [filteredAttendanceStats, setFilteredAttendanceStats] = useState<AttendanceStats | null>(null);
  const [filteredTutorAttendanceStats, setFilteredTutorAttendanceStats] = useState<TutorAttendanceStats | null>(null);
  const [selectedView, setSelectedView] = useState<'estudiantes' | 'tutores'>('estudiantes');
  const [showCreateSchoolTeamForm, setShowCreateSchoolTeamForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { fetchWithAuth, user } = useAuth();

  const fetchEquipos = async () => {
    if (user?.rol === 'admin') {
      try {
        const equiposResponse = await fetchWithAuth('/equipos/');
        if (equiposResponse.ok) {
          const equiposData = await equiposResponse.json();
          setEquipos(equiposData);
        }
      } catch (err) {
        console.error('Error al cargar equipos:', err);
      }
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Cargar estudiantes
        const estudiantesResponse = await fetchWithAuth('/estudiantes/');
        if (estudiantesResponse.ok) {
          const estudiantesData = await estudiantesResponse.json();
          setEstudiantes(estudiantesData);
        }

        // Cargar tutores
        const tutoresResponse = await fetchWithAuth('/tutores/');
        if (tutoresResponse.ok) {
          const tutoresData = await tutoresResponse.json();
          setTutores(tutoresData);
        }

        // Cargar equipos (solo si es admin)
        await fetchEquipos();

        // Cargar estadísticas de asistencia de estudiantes
        const attendanceResponse = await fetchWithAuth('/attendance/students/attendance-stats');
        if (attendanceResponse.ok) {
          const attendanceData = await attendanceResponse.json();
          setAttendanceStats(attendanceData);
        }

        // Cargar estadísticas de asistencia de tutores
        const tutorAttendanceResponse = await fetchWithAuth('/attendance/tutors/attendance-stats');
        if (tutorAttendanceResponse.ok) {
          const tutorAttendanceData = await tutorAttendanceResponse.json();
          setTutorAttendanceStats(tutorAttendanceData);
        }

      } catch (err) {
        console.error('Error cargando datos:', err);
        setError('Error de conexión al cargar datos');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, fetchWithAuth]);

  // Filtrar estadísticas de asistencia de estudiantes por equipo cuando cambien los estudiantes
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

  // Filtrar estadísticas de asistencia de tutores por equipo cuando cambien los tutores
  useEffect(() => {
    if (tutorAttendanceStats && tutores.length > 0) {
      if (user?.rol === 'tutor' && user?.equipo_id) {
        // Filtrar solo los tutores del equipo del tutor
        const filteredStats = tutorAttendanceStats.tutors_stats.filter((tutorStat: any) => {
          const tutor = tutores.find(t => t.id === tutorStat.tutor_id);
          return tutor && tutor.equipo_id === user.equipo_id;
        });
        
        const filteredAbsences = tutorAttendanceStats.tutors_with_3_plus_absences.filter((tutorStat: any) => {
          const tutor = tutores.find(t => t.id === tutorStat.tutor_id);
          return tutor && tutor.equipo_id === user.equipo_id;
        });
        
        // Recalcular promedio solo para el equipo
        const totalAttended = filteredStats.reduce((sum: number, tutorStat: any) => sum + tutorStat.attended_weeks, 0);
        const totalPossible = filteredStats.reduce((sum: number, tutorStat: any) => sum + tutorStat.total_weeks, 0);
        const teamAverage = totalPossible > 0 ? (totalAttended / totalPossible) * 100 : 0;
        
        setFilteredTutorAttendanceStats({
          tutors_stats: filteredStats,
          overall_average: Math.round(teamAverage * 100) / 100,
          tutors_with_3_plus_absences: filteredAbsences,
          total_tutors: filteredStats.length
        });
      } else {
        // Si es admin, mostrar todos los datos
        setFilteredTutorAttendanceStats(tutorAttendanceStats);
      }
    }
  }, [tutorAttendanceStats, tutores, user]);

  const getEquipoNombre = (equipoId: number) => {
    const equipo = equipos.find(e => e.id === equipoId);
    return equipo ? equipo.nombre : `Equipo ${equipoId}`;
  };

  const getColegioNombre = (equipoId: number) => {
    const equipo = equipos.find(e => e.id === equipoId);
    return equipo?.colegio?.nombre || 'Sin colegio';
  };

  const handleCreateSuccess = () => {
    // Recargar equipos y colegios
    fetchEquipos();
    setShowCreateSchoolTeamForm(false);
  };

  return (
    <div className="page-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 className="page-title" style={{ margin: 0 }}>Dashboard</h1>
        {user?.rol === 'admin' && (
          <button
            className="btn btn-primary"
            onClick={() => setShowCreateSchoolTeamForm(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            ➕ Crear Colegio y Equipo
          </button>
        )}
      </div>

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
          {/* Estadísticas generales - Primera fila: Estudiantes, Equipos (centro), Tutores */}
          <div className="stats-section">
            <div className="stats-grid-top-row">
              <div className="stat-card-compact stat-card-students">
                <h3>Estudiantes</h3>
                <p className="stat-number">{estudiantes.length}</p>
                {user?.rol === 'tutor' && (
                  <p className="stat-detail">en tu equipo</p>
                )}
              </div>
              
              {user?.rol === 'admin' && (
                <div className="stat-card-compact stat-card-center">
                  <h3>Equipos</h3>
                  <p className="stat-number">{equipos.length}</p>
                </div>
              )}
              
              <div className="stat-card-compact stat-card-tutors">
                <h3>Tutores</h3>
                <p className="stat-number">{tutores.length}</p>
                {user?.rol === 'tutor' && (
                  <p className="stat-detail">en tu equipo</p>
                )}
              </div>
            </div>
          </div>

          {/* Promedios de Asistencia - Segunda fila: Estudiantes (izq), Tutores (der) */}
          <div className="attendance-stats-compact">
            <div className="stats-grid-two-columns">
              {filteredAttendanceStats && (
                <div className="attendance-card-small attendance-card-students">
                  <h3>Promedio % Asistencia Estudiantes</h3>
                  <p className="stat-number-small">
                    {filteredAttendanceStats.overall_average}%
                  </p>
                  <p className="stat-detail-small">
                    {filteredAttendanceStats.total_students} estudiantes
                  </p>
                </div>
              )}
              
              {filteredTutorAttendanceStats && (
                <div className="attendance-card-small attendance-card-tutors">
                  <h3>Promedio % Asistencia Tutores</h3>
                  <p className="stat-number-small">
                    {filteredTutorAttendanceStats.overall_average}%
                  </p>
                  <p className="stat-detail-small">
                    {filteredTutorAttendanceStats.total_tutors} tutores
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Inasistencias - Tercera fila: Estudiantes (izq), Tutores (der) */}
          <div className="attendance-stats-compact">
            <div className="stats-grid-two-columns">
              {filteredAttendanceStats && (
                <div className="warning-card-small warning-card-students">
                  <h3>+3 Inasistencias Estudiantes</h3>
                  <p className="stat-number-small">
                    {filteredAttendanceStats.students_with_3_plus_absences.length}
                  </p>
                  <p className="stat-detail-small">requieren atención</p>
                </div>
              )}
              
              {filteredTutorAttendanceStats && (
                <div className="warning-card-small warning-card-tutors">
                  <h3>+3 Inasistencias Tutores</h3>
                  <p className="stat-number-small">
                    {filteredTutorAttendanceStats.tutors_with_3_plus_absences.length}
                  </p>
                  <p className="stat-detail-small">requieren atención</p>
                </div>
              )}
            </div>
          </div>

          {/* Selector de vista y contenido condicional */}
          <div className="view-selector-section">
            <div className="view-selector">
              <button
                className={`view-button ${selectedView === 'estudiantes' ? 'active' : ''}`}
                onClick={() => setSelectedView('estudiantes')}
              >
                Estudiantes
              </button>
              <button
                className={`view-button ${selectedView === 'tutores' ? 'active' : ''}`}
                onClick={() => setSelectedView('tutores')}
              >
                Tutores
              </button>
            </div>
          </div>

          {/* Contenido para Estudiantes */}
          {selectedView === 'estudiantes' && filteredAttendanceStats && (
            <>
              {/* Gráfico de Asistencia de Estudiantes */}
              <div className="attendance-chart-section">
                <h2 className="section-title">Gráfico de Asistencia por Estudiante</h2>
                <div className="chart-container">
                  <AttendanceChart 
                    data={filteredAttendanceStats.students_stats}
                    title="Porcentaje de Asistencia por Estudiante"
                    xAxisLabel="Estudiantes"
                  />
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
            </>
          )}

          {/* Contenido para Tutores */}
          {selectedView === 'tutores' && filteredTutorAttendanceStats && (
            <>
              {/* Gráfico de Asistencia de Tutores */}
              <div className="attendance-chart-section">
                <h2 className="section-title">Gráfico de Asistencia por Tutor</h2>
                <div className="chart-container">
                  <AttendanceChart 
                    data={filteredTutorAttendanceStats.tutors_stats.map(tutor => ({
                      student_id: tutor.tutor_id,
                      student_name: tutor.tutor_name,
                      attendance_percentage: tutor.attendance_percentage,
                      attended_weeks: tutor.attended_weeks,
                      absent_weeks: tutor.absent_weeks,
                      total_weeks: tutor.total_weeks
                    }))}
                    title="Porcentaje de Asistencia por Tutor"
                    xAxisLabel="Tutores"
                  />
                </div>
              </div>

              {/* Lista de Tutores con muchas inasistencias */}
              {filteredTutorAttendanceStats.tutors_with_3_plus_absences.length > 0 && (
                <div className="students-absences-section">
                  <h2 className="section-title">Tutores con más de 3 Inasistencias</h2>
                  <div className="absences-list">
                    {filteredTutorAttendanceStats.tutors_with_3_plus_absences.map((tutor) => (
                      <div key={tutor.tutor_id} className="absence-card">
                        <h4>{tutor.tutor_name}</h4>
                        <p className="absence-count">
                          Inasistencias: {tutor.absent_weeks}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tabla de tutores */}
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
            </>
          )}

        </> 
      )}

      {showCreateSchoolTeamForm && (
        <CreateSchoolTeamForm
          onSuccess={handleCreateSuccess}
          onClose={() => setShowCreateSchoolTeamForm(false)}
        />
      )}
    </div>
  );
};

export default Dashboard;
