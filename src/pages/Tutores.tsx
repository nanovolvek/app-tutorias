import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AddTutorForm from '../components/AddTutorForm';
import DeleteTutorForm from '../components/DeleteTutorForm';
import ImportTutorForm from '../components/ImportTutorForm';
import { useIsMobile } from '../hooks/useIsMobile';

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
  const [showImportForm, setShowImportForm] = useState(false);
  const [expandedTutores, setExpandedTutores] = useState<Set<number>>(new Set());
  const isMobile = useIsMobile();

  const toggleTutor = (tutorId: number) => {
    setExpandedTutores(prev => {
      const newSet = new Set(prev);
      if (newSet.has(tutorId)) {
        newSet.delete(tutorId);
      } else {
        newSet.add(tutorId);
      }
      return newSet;
    });
  };

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
          <button 
            className="btn btn-info" 
            onClick={() => setShowImportForm(true)}
          >
            📥 Importar Excel
          </button>
        </div>
      </div>

      {tutores.length === 0 ? (
        <div className="no-data">
          <p>No hay tutores registrados</p>
        </div>
      ) : (
        <>
          {isMobile ? (
            <div className="mobile-cards-container">
              {tutores.map((tutor) => {
                const attendancePercentage = getAttendancePercentage(tutor);
                const isExpanded = expandedTutores.has(tutor.id);
                return (
                  <div key={tutor.id} className="mobile-card">
                    <div 
                      className="mobile-card-header"
                      onClick={() => toggleTutor(tutor.id)}
                    >
                      <div className="mobile-card-title">
                        <div className="mobile-card-name">{tutor.nombre} {tutor.apellido}</div>
                      </div>
                      <div className="mobile-card-arrow">
                        {isExpanded ? '▼' : '▶'}
                      </div>
                    </div>
                    {isExpanded && (
                      <div className="mobile-card-content">
                        <div className="mobile-card-row">
                          <span className="mobile-card-label">Email:</span>
                          <span className="mobile-card-value">{tutor.email}</span>
                        </div>
                        <div className="mobile-card-row">
                          <span className="mobile-card-label">Equipo:</span>
                          <span className="mobile-card-value">{tutor.equipo?.nombre || 'Sin equipo'}</span>
                        </div>
                        <div className="mobile-card-row">
                          <span className="mobile-card-label">Colegio:</span>
                          <span className="mobile-card-value">{getColegioNombre(tutor)}</span>
                        </div>
                        <div className="mobile-card-row">
                          <span className="mobile-card-label">Comuna:</span>
                          <span className="mobile-card-value">{getComunaNombre(tutor)}</span>
                        </div>
                        <div className="mobile-card-row">
                          <span className="mobile-card-label">% Asistencia:</span>
                          <span className={`mobile-card-value attendance-cell ${getAttendanceColor(attendancePercentage)}`}>
                            {attendancePercentage.toFixed(1)}%
                          </span>
                        </div>
                        <div className="mobile-card-row">
                          <span className="mobile-card-label">Activo:</span>
                          <span className="mobile-card-value">
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
                          </span>
                        </div>
                        <div className="mobile-card-row">
                          <span className="mobile-card-label">Motivo Deserción:</span>
                          <span className="mobile-card-value">{tutor.motivo_desercion || 'N/A'}</span>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th className="sticky-col-1">Nombre Completo</th>
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
                  {tutores.map((tutor) => {
                    const attendancePercentage = getAttendancePercentage(tutor);
                    return (
                      <tr key={tutor.id}>
                        <td className="sticky-col-1">{tutor.nombre} {tutor.apellido}</td>
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
                  })}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

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

      {showImportForm && (
        <ImportTutorForm
          onSuccess={handleAddSuccess}
          onClose={() => setShowImportForm(false)}
        />
      )}
    </div>
  );
};

export default Tutores;