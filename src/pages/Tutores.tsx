import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AddTutorForm from '../components/AddTutorForm';
import DeleteTutorForm from '../components/DeleteTutorForm';

interface Equipo {
  id: number;
  nombre: string;
  colegio?: {
    id: number;
    nombre: string;
    comuna: string;
  };
}

interface Tutor {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  equipo_id: number;
  activo?: boolean;
  motivo_desercion?: string;
  created_at: string;
  equipo?: Equipo;
}

const Tutores: React.FC = () => {
  const { fetchWithAuth } = useAuth();
  const [tutores, setTutores] = useState<Tutor[]>([]);
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [attendanceStats, setAttendanceStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [showDeleteForm, setShowDeleteForm] = useState(false);

  const fetchTutores = async () => {
    try {
      const response = await fetchWithAuth('/tutores/');
      if (response.ok) {
        const data = await response.json();
        setTutores(data);
      } else {
        setError('Error al cargar los tutores');
      }
    } catch (error) {
      console.error('Error al cargar tutores:', error);
      setError('Error de conexión al cargar los tutores');
    } finally {
      setLoading(false);
    }
  };

  const fetchAttendanceStats = async () => {
    try {
      const response = await fetchWithAuth('/attendance/tutors/attendance-stats');
      if (response.ok) {
        const data = await response.json();
        setAttendanceStats(data);
      }
    } catch (error) {
      console.error('Error al cargar estadísticas de asistencia:', error);
    }
  };

  const fetchEquipos = async () => {
    try {
      const response = await fetchWithAuth('/equipos/');
      if (response.ok) {
        const data = await response.json();
        setEquipos(data);
      }
    } catch (error) {
      console.error('Error al cargar equipos:', error);
    }
  };

  useEffect(() => {
    fetchTutores();
    fetchEquipos();
    fetchAttendanceStats();
  }, []);

  const getAttendancePercentage = (tutor: Tutor) => {
    if (!attendanceStats) return 0;
    const tutorStats = attendanceStats.tutors_stats.find((t: any) => t.tutor_id === tutor.id);
    return tutorStats ? tutorStats.attendance_percentage : 0;
  };

  const getAttendanceColor = (percentage: number) => {
    if (percentage >= 80) return 'attendance-high';
    if (percentage >= 60) return 'attendance-medium';
    return 'attendance-low';
  };

  const handleAddSuccess = () => {
    fetchTutores();
  };

  const handleDeleteSuccess = () => {
    fetchTutores();
  };

  const getColegioNombre = (tutor: Tutor) => {
    return tutor.equipo?.colegio?.nombre || 'Sin colegio';
  };

  const getComunaNombre = (tutor: Tutor) => {
    return tutor.equipo?.colegio?.comuna || 'Sin comuna';
  };

  const handleExportExcel = async () => {
    try {
      const XLSX = await import('xlsx');
      
      // Preparar datos para Excel
      const excelData = [
        // Encabezados
        ['Nombre Completo', 'Email', 'Equipo', 'Colegio', 'Comuna', '% Asistencia', 'Activo', 'Motivo Deserción', 'Fecha Registro'],
        // Tutores
        ...tutores.map(tutor => [
          `${tutor.nombre} ${tutor.apellido}`,
          tutor.email,
          tutor.equipo?.nombre || 'Sin equipo',
          getColegioNombre(tutor),
          getComunaNombre(tutor),
          `${getAttendancePercentage(tutor).toFixed(1)}%`,
          tutor.activo !== false ? 'Sí' : 'No',
          tutor.motivo_desercion || 'N/A',
          new Date(tutor.created_at).toLocaleDateString('es-ES')
        ])
      ];
      
      // Crear libro de Excel
      const ws = XLSX.utils.aoa_to_sheet(excelData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Tutores');
      
      // Descargar archivo
      const fileName = `tutores_${new Date().toISOString().split('T')[0]}.xlsx`;
      XLSX.writeFile(wb, fileName);
      
    } catch (error) {
      console.error('Error al exportar Excel:', error);
      setError('Error al exportar el archivo Excel');
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <h1 className="page-title">Tutores</h1>
        <div className="loading">Cargando tutores...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <h1 className="page-title">Tutores</h1>
        <div className="error-message">
          <p>{error}</p>
          <button onClick={fetchTutores} className="btn btn-primary">
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <h1 className="page-title">Tutores</h1>
      <p className="page-description">
        Gestiona los tutores del sistema. Aquí puedes ver, agregar, eliminar y exportar información de los tutores.
      </p>

      <div className="section-header">
        <h2 className="section-title">Lista de Tutores</h2>
        <div className="action-buttons">
          <button 
            className="btn btn-primary" 
            onClick={() => setShowAddForm(true)}
          >
            Agregar Tutor
          </button>
          <button 
            className="btn btn-danger" 
            onClick={() => setShowDeleteForm(true)}
          >
            Eliminar Tutor
          </button>
          <button 
            className="btn btn-success" 
            onClick={handleExportExcel}
          >
            Exportar Excel
          </button>
        </div>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Nombre Completo</th>
              <th>Email</th>
              <th>Equipo</th>
              <th>Colegio</th>
              <th>Comuna</th>
              <th>% Asistencia</th>
              <th>Activo</th>
              <th>Motivo Deserción</th>
            </tr>
          </thead>
          <tbody>
            {tutores.length === 0 ? (
              <tr>
                <td colSpan={8} className="text-center">
                  No hay tutores registrados
                </td>
              </tr>
            ) : (
              tutores.map((tutor) => {
                const attendancePercentage = getAttendancePercentage(tutor);
                return (
                  <tr key={tutor.id}>
                    <td>{tutor.nombre} {tutor.apellido}</td>
                    <td>{tutor.email}</td>
                    <td>{tutor.equipo?.nombre || 'Sin equipo'}</td>
                    <td>{getColegioNombre(tutor)}</td>
                    <td>{getComunaNombre(tutor)}</td>
                    <td className={`attendance-cell ${getAttendanceColor(attendancePercentage)}`}>
                      {attendancePercentage.toFixed(1)}%
                    </td>
                    <td>
                      <span style={{
                        padding: '4px 8px',
                        borderRadius: '4px',
                        fontSize: '0.85rem',
                        fontWeight: '600',
                        backgroundColor: tutor.activo !== false ? '#dcfce7' : '#fee2e2',
                        color: tutor.activo !== false ? '#166534' : '#991b1b'
                      }}>
                        {tutor.activo !== false ? 'Sí' : 'No'}
                      </span>
                    </td>
                    <td>{tutor.motivo_desercion || 'N/A'}</td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {showAddForm && (
        <AddTutorForm
          onSuccess={handleAddSuccess}
          onClose={() => setShowAddForm(false)}
          equipos={equipos}
        />
      )}

      {showDeleteForm && (
        <DeleteTutorForm
          onSuccess={handleDeleteSuccess}
          onClose={() => setShowDeleteForm(false)}
          tutores={tutores}
        />
      )}
    </div>
  );
};

export default Tutores;