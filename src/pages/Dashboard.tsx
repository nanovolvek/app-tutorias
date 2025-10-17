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
}

const Dashboard: React.FC = () => {
  const [estudiantes, setEstudiantes] = useState<Estudiante[]>([]);
  const [tutores, setTutores] = useState<Tutor[]>([]);
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token, user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        
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

  const getEquipoNombre = (equipoId: number) => {
    const equipo = equipos.find(e => e.id === equipoId);
    return equipo ? equipo.nombre : `Equipo ${equipoId}`;
  };

  return (
    <div className="page-container">
      <h1 className="page-title">Dashboard</h1>
      <p className="page-description">
        Bienvenido a la Plataforma de Tutorías. Aquí podrás ver un resumen general 
        del programa y acceso rápido a las funciones principales.
      </p>

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
          {/* Información del usuario */}
          <div className="user-info">
            <h2>Bienvenido, {user?.nombre_completo}</h2>
            <p>Rol: {user?.rol === 'admin' ? 'Administrador' : 'Tutor'}</p>
            {user?.equipo_id && (
              <p>Equipo: {getEquipoNombre(user.equipo_id)}</p>
            )}
          </div>

          {/* Estadísticas generales */}
          <div className="stats-section">
            <h2 className="section-title">Estadísticas</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Estudiantes</h3>
                <p className="stat-number">{estudiantes.length}</p>
                {user?.rol === 'tutor' && (
                  <p className="stat-detail">en tu equipo</p>
                )}
              </div>
              
              <div className="stat-card">
                <h3>Tutores</h3>
                <p className="stat-number">{tutores.length}</p>
                {user?.rol === 'tutor' && (
                  <p className="stat-detail">en tu equipo</p>
                )}
              </div>

              {user?.rol === 'admin' && (
                <div className="stat-card">
                  <h3>Equipos</h3>
                  <p className="stat-number">{equipos.length}</p>
                </div>
              )}
            </div>
          </div>

          {/* Lista de estudiantes */}
          <div className="students-section">
            <h2 className="section-title">Estudiantes</h2>
            {estudiantes.length > 0 ? (
              <div className="students-grid">
                {estudiantes.map((estudiante) => (
                  <div key={estudiante.id} className="student-card">
                    <h4>{estudiante.nombre} {estudiante.apellido}</h4>
                    <p>Curso: {estudiante.curso}</p>
                    <p>Equipo: {getEquipoNombre(estudiante.equipo_id)}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p>No hay estudiantes disponibles</p>
            )}
          </div>

          {/* Lista de tutores (solo para admin) */}
          {user?.rol === 'admin' && (
            <div className="tutors-section">
              <h2 className="section-title">Tutores</h2>
              {tutores.length > 0 ? (
                <div className="tutors-grid">
                  {tutores.map((tutor) => (
                    <div key={tutor.id} className="tutor-card">
                      <h4>{tutor.nombre} {tutor.apellido}</h4>
                      <p>Equipo: {getEquipoNombre(tutor.equipo_id)}</p>
                    </div>
                  ))}
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
