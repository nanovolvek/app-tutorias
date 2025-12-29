import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AddStudentForm from '../components/AddStudentForm';
import DeleteStudentForm from '../components/DeleteStudentForm';
import ImportStudentForm from '../components/ImportStudentForm';
import { useIsMobile } from '../hooks/useIsMobile';

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

interface Student {
  id: number;
  rut: string;
  nombre: string;
  apellido: string;
  curso: string;
  equipo_id: number;
  nombre_apoderado?: string;
  contacto_apoderado?: string;
  observaciones?: string;
  activo?: boolean;
  motivo_desercion?: string;
  equipo: Equipo;
  created_at: string;
  updated_at?: string;
  attendance_percentage?: number;
}

const Estudiantes: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [showDeleteForm, setShowDeleteForm] = useState(false);
  const [showImportForm, setShowImportForm] = useState(false);
  const [attendanceStats, setAttendanceStats] = useState<any>(null);
  const [expandedStudents, setExpandedStudents] = useState<Set<number>>(new Set());
  const isMobile = useIsMobile();
  const { fetchWithAuth, user } = useAuth();

  const toggleStudent = (studentId: number) => {
    setExpandedStudents(prev => {
      const newSet = new Set(prev);
      if (newSet.has(studentId)) {
        newSet.delete(studentId);
      } else {
        newSet.add(studentId);
      }
      return newSet;
    });
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Cargar estudiantes
        const studentsResponse = await fetchWithAuth('/estudiantes/');
        if (studentsResponse.ok) {
          const studentsData = await studentsResponse.json();
          console.log('Estudiantes recibidos:', studentsData);
          
          // Filtrar estudiantes por equipo si es tutor
          if (user?.rol === 'tutor' && user?.equipo_id) {
            const filteredStudents = studentsData.filter((student: Student) => 
              student.equipo_id === user.equipo_id
            );
            setStudents(filteredStudents);
          } else {
            setStudents(studentsData);
          }
        } else {
          setError('Error al cargar los estudiantes');
        }

        // Cargar estadísticas de asistencia
        const attendanceResponse = await fetchWithAuth('/attendance/students/attendance-stats');
        if (attendanceResponse.ok) {
          const attendanceData = await attendanceResponse.json();
          setAttendanceStats(attendanceData);
        }
      } catch (err) {
        console.error('Error:', err);
        setError('Error de conexión');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user]);

  const getColegioNombre = (student: Student) => {
    return student.equipo?.colegio?.nombre || 'Sin colegio';
  };

  const getComunaNombre = (student: Student) => {
    return student.equipo?.colegio?.comuna || 'Sin comuna';
  };

  const getAttendancePercentage = (student: Student) => {
    if (!attendanceStats) return 0;
    const studentStats = attendanceStats.students_stats.find((s: any) => s.student_id === student.id);
    return studentStats ? studentStats.attendance_percentage : 0;
  };

  const getAttendanceColor = (percentage: number) => {
    if (percentage >= 80) return 'attendance-high';
    if (percentage >= 60) return 'attendance-medium';
    return 'attendance-low';
  };

  const handleAddSuccess = () => {
    // Recargar datos
    window.location.reload();
  };

  const handleDeleteSuccess = () => {
    // Recargar datos
    window.location.reload();
  };

  const handleExportExcel = async () => {
    try {
      const XLSX = await import('xlsx');
      
      // Preparar datos para Excel
      const excelData = [
        // Encabezados
        ['RUT', 'Nombre Completo', 'Curso', 'Equipo', 'Colegio', 'Comuna', '% Asistencia', 'Activo', 'Motivo Deserción', 'Apoderado', 'Contacto', 'Observaciones', 'Fecha Registro'],
        // Estudiantes
        ...students.map(student => [
          student.rut,
          `${student.nombre} ${student.apellido}`,
          student.curso,
          student.equipo?.nombre || 'Sin equipo',
          getColegioNombre(student),
          getComunaNombre(student),
          `${getAttendancePercentage(student).toFixed(1)}%`,
          student.activo !== false ? 'Sí' : 'No',
          student.motivo_desercion || 'N/A',
          student.nombre_apoderado || 'N/A',
          student.contacto_apoderado || 'N/A',
          student.observaciones || 'N/A',
          new Date(student.created_at).toLocaleDateString('es-ES')
        ])
      ];
      
      // Crear libro de Excel
      const ws = XLSX.utils.aoa_to_sheet(excelData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Estudiantes');
      
      // Descargar archivo
      const fileName = `estudiantes_${new Date().toISOString().split('T')[0]}.xlsx`;
      XLSX.writeFile(wb, fileName);
      
    } catch (error) {
      console.error('Error al exportar Excel:', error);
      setError('Error al exportar el archivo Excel');
    }
  };

  return (
    <div className="page-container">
      <h1 className="page-title">Estudiantes</h1>
      <p className="page-description">
        Gestiona la información de todos los estudiantes del programa de tutorías. 
        Aquí podrás consultar datos personales, historial académico y estado actual.
      </p>

      <div className="students-section">
        <div className="section-header">
          <h2 className="section-title">Lista de Estudiantes</h2>
          <div className="action-buttons">
            <button 
              className="btn btn-primary" 
              onClick={() => setShowAddForm(true)}
            >
              ➕ Agregar Estudiante
            </button>
            <button 
              className="btn btn-danger" 
              onClick={() => setShowDeleteForm(true)}
            >
              Eliminar Estudiante
            </button>
            <button 
              className="btn btn-success" 
              onClick={handleExportExcel}
            >
              📊 Exportar Excel
            </button>
            <button 
              className="btn btn-info" 
              onClick={() => setShowImportForm(true)}
            >
              📥 Importar Excel
            </button>
          </div>
        </div>
        
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
          <>
            {isMobile ? (
              <div className="mobile-cards-container">
                {students.map((student) => {
                  const attendancePercentage = getAttendancePercentage(student);
                  const isExpanded = expandedStudents.has(student.id);
                  return (
                    <div key={student.id} className="mobile-card">
                      <div 
                        className="mobile-card-header"
                        onClick={() => toggleStudent(student.id)}
                      >
                        <div className="mobile-card-title">
                          <div className="mobile-card-rut">{student.rut}</div>
                          <div className="mobile-card-name">{student.nombre} {student.apellido}</div>
                        </div>
                        <div className="mobile-card-arrow">
                          {isExpanded ? '▼' : '▶'}
                        </div>
                      </div>
                      {isExpanded && (
                        <div className="mobile-card-content">
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Curso:</span>
                            <span className="mobile-card-value">{student.curso}</span>
                          </div>
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Equipo:</span>
                            <span className="mobile-card-value">{student.equipo?.nombre || 'Sin equipo'}</span>
                          </div>
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Colegio:</span>
                            <span className="mobile-card-value">{getColegioNombre(student)}</span>
                          </div>
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Comuna:</span>
                            <span className="mobile-card-value">{getComunaNombre(student)}</span>
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
                                backgroundColor: student.activo !== false ? '#dcfce7' : '#fee2e2',
                                color: student.activo !== false ? '#166534' : '#991b1b'
                              }}>
                                {student.activo !== false ? 'Sí' : 'No'}
                              </span>
                            </span>
                          </div>
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Motivo Deserción:</span>
                            <span className="mobile-card-value">{student.motivo_desercion || 'N/A'}</span>
                          </div>
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Apoderado:</span>
                            <span className="mobile-card-value">{student.nombre_apoderado || 'N/A'}</span>
                          </div>
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Contacto:</span>
                            <span className="mobile-card-value">{student.contacto_apoderado || 'N/A'}</span>
                          </div>
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Observaciones:</span>
                            <span className="mobile-card-value">{student.observaciones || 'N/A'}</span>
                          </div>
                          <div className="mobile-card-row">
                            <span className="mobile-card-label">Fecha de Registro:</span>
                            <span className="mobile-card-value">{new Date(student.created_at).toLocaleDateString('es-ES')}</span>
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
                      <th className="sticky-col-1">RUT</th>
                      <th className="sticky-col-2">Nombre Completo</th>
                      <th>Curso</th>
                      <th>Equipo</th>
                      <th>Colegio</th>
                      <th>Comuna</th>
                      <th>% Asistencia</th>
                      <th>Activo</th>
                      <th>Motivo Deserción</th>
                      <th>Apoderado</th>
                      <th>Contacto</th>
                      <th>Observaciones</th>
                      <th>Fecha de Registro</th>
                    </tr>
                  </thead>
                  <tbody>
                    {students.map((student) => {
                      const attendancePercentage = getAttendancePercentage(student);
                      return (
                        <tr key={student.id}>
                          <td className="rut-cell sticky-col-1">{student.rut}</td>
                          <td className="name-cell sticky-col-2">{student.nombre} {student.apellido}</td>
                          <td>{student.curso}</td>
                          <td>{student.equipo?.nombre || 'Sin equipo'}</td>
                          <td>{getColegioNombre(student)}</td>
                          <td>{getComunaNombre(student)}</td>
                          <td className={`attendance-cell ${getAttendanceColor(attendancePercentage)}`}>
                            {attendancePercentage.toFixed(1)}%
                          </td>
                          <td>
                            <span style={{
                              padding: '4px 8px',
                              borderRadius: '4px',
                              fontSize: '0.85rem',
                              fontWeight: '600',
                              backgroundColor: student.activo !== false ? '#dcfce7' : '#fee2e2',
                              color: student.activo !== false ? '#166534' : '#991b1b'
                            }}>
                              {student.activo !== false ? 'Sí' : 'No'}
                            </span>
                          </td>
                          <td>{student.motivo_desercion || 'N/A'}</td>
                          <td>{student.nombre_apoderado || 'N/A'}</td>
                          <td>{student.contacto_apoderado || 'N/A'}</td>
                          <td className="observations-cell">{student.observaciones || 'N/A'}</td>
                          <td>{new Date(student.created_at).toLocaleDateString('es-ES')}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </div>

      {/* Modal para agregar estudiante */}
      {showAddForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Agregar Nuevo Estudiante</h3>
              <button 
                className="modal-close" 
                onClick={() => setShowAddForm(false)}
              >
                ✕
              </button>
            </div>
            <AddStudentForm 
              onClose={() => setShowAddForm(false)}
              onSuccess={() => {
                setShowAddForm(false);
                // Recargar datos
                window.location.reload();
              }}
              user={user}
            />
          </div>
        </div>
      )}

      {/* Modal para eliminar estudiante */}
      {showDeleteForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Eliminar Estudiante</h3>
              <button 
                className="modal-close" 
                onClick={() => setShowDeleteForm(false)}
              >
                ✕
              </button>
            </div>
            <DeleteStudentForm 
              students={students}
              onClose={() => setShowDeleteForm(false)}
              onSuccess={handleDeleteSuccess}
            />
          </div>
        </div>
      )}

      {showImportForm && (
        <ImportStudentForm
          onSuccess={handleAddSuccess}
          onClose={() => setShowImportForm(false)}
        />
      )}
    </div>
  );
};

export default Estudiantes;
