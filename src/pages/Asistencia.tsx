import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Asistencia.css';

interface Week {
  semana_numero: number;
  semana_key: string;
  mes: string;
  dias: string;
  fecha_inicio: string;
  fecha_fin: string;
  mes_numero: number;
}

interface Student {
  id: number;
  nombre: string;
  apellido: string;
  colegio_id: number;
  equipo_id: number;
}

interface Tutor {
  id: number;
  nombre: string;
  apellido: string;
  colegio_id: number;
  equipo_id: number;
}

interface School {
  id: number;
  nombre: string;
}

interface Equipo {
  id: number;
  nombre: string;
}

interface AttendanceRecord {
  id: number;
  semana: string;
  mes: string;
  dias: string;
  estado: string | null;
}

const Asistencia: React.FC = () => {
  const { token, user } = useAuth();
  
  // Estados
  const [weeks, setWeeks] = useState<Week[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [tutors, setTutors] = useState<Tutor[]>([]);
  const [schools, setSchools] = useState<School[]>([]);
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<number | null>(null);
  const [selectedTutor, setSelectedTutor] = useState<number | null>(null);
  const [selectedSchool, setSelectedSchool] = useState<number | null>(null);
  const [selectedEquipo, setSelectedEquipo] = useState<number | null>(null);
  const [selectedMonth, setSelectedMonth] = useState<string | null>(null);
  const [selectedPersonType, setSelectedPersonType] = useState<'estudiante' | 'tutor' | null>(null);
  const [attendanceRecords, setAttendanceRecords] = useState<AttendanceRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [editingWeek, setEditingWeek] = useState<string | null>(null);
  const [editingPerson, setEditingPerson] = useState<number | null>(null);

  // Estados de asistencia
  const attendanceStates = [
    { key: 'asistió', label: 'Asistió', color: '#10B981' },
    { key: 'no asistió', label: 'No asistió', color: '#EF4444' },
    { key: 'tutoría suspendida', label: 'Suspendida', color: '#F59E0B' },
    { key: 'vacaciones/feriado', label: 'Vacaciones/Feriado', color: '#6B7280' }
  ];

  // Datos mock del calendario 2026
  const mockWeeks: Week[] = [
    { semana_numero: 1, semana_key: "semana_1", mes: "Marzo", dias: "2 al 8", fecha_inicio: "2026-03-02", fecha_fin: "2026-03-08", mes_numero: 3 },
    { semana_numero: 2, semana_key: "semana_2", mes: "Marzo", dias: "9 al 15", fecha_inicio: "2026-03-09", fecha_fin: "2026-03-15", mes_numero: 3 },
    { semana_numero: 3, semana_key: "semana_3", mes: "Marzo", dias: "16 al 22", fecha_inicio: "2026-03-16", fecha_fin: "2026-03-22", mes_numero: 3 },
    { semana_numero: 4, semana_key: "semana_4", mes: "Marzo", dias: "23 al 29", fecha_inicio: "2026-03-23", fecha_fin: "2026-03-29", mes_numero: 3 },
    { semana_numero: 5, semana_key: "semana_5", mes: "Marzo", dias: "30 al 5", fecha_inicio: "2026-03-30", fecha_fin: "2026-04-05", mes_numero: 3 },
    { semana_numero: 6, semana_key: "semana_6", mes: "Abril", dias: "6 al 12", fecha_inicio: "2026-04-06", fecha_fin: "2026-04-12", mes_numero: 4 },
    { semana_numero: 7, semana_key: "semana_7", mes: "Abril", dias: "13 al 19", fecha_inicio: "2026-04-13", fecha_fin: "2026-04-19", mes_numero: 4 },
    { semana_numero: 8, semana_key: "semana_8", mes: "Abril", dias: "20 al 26", fecha_inicio: "2026-04-20", fecha_fin: "2026-04-26", mes_numero: 4 },
    { semana_numero: 9, semana_key: "semana_9", mes: "Abril", dias: "27 al 3", fecha_inicio: "2026-04-27", fecha_fin: "2026-05-03", mes_numero: 4 },
    { semana_numero: 10, semana_key: "semana_10", mes: "Mayo", dias: "4 al 10", fecha_inicio: "2026-05-04", fecha_fin: "2026-05-10", mes_numero: 5 },
    { semana_numero: 11, semana_key: "semana_11", mes: "Mayo", dias: "11 al 17", fecha_inicio: "2026-05-11", fecha_fin: "2026-05-17", mes_numero: 5 },
    { semana_numero: 12, semana_key: "semana_12", mes: "Mayo", dias: "18 al 24", fecha_inicio: "2026-05-18", fecha_fin: "2026-05-24", mes_numero: 5 },
    { semana_numero: 13, semana_key: "semana_13", mes: "Mayo", dias: "25 al 31", fecha_inicio: "2026-05-25", fecha_fin: "2026-05-31", mes_numero: 5 },
    { semana_numero: 14, semana_key: "semana_14", mes: "Junio", dias: "1 al 7", fecha_inicio: "2026-06-01", fecha_fin: "2026-06-07", mes_numero: 6 },
    { semana_numero: 15, semana_key: "semana_15", mes: "Junio", dias: "8 al 14", fecha_inicio: "2026-06-08", fecha_fin: "2026-06-14", mes_numero: 6 },
    { semana_numero: 16, semana_key: "semana_16", mes: "Junio", dias: "15 al 21", fecha_inicio: "2026-06-15", fecha_fin: "2026-06-21", mes_numero: 6 },
    { semana_numero: 17, semana_key: "semana_17", mes: "Junio", dias: "22 al 28", fecha_inicio: "2026-06-22", fecha_fin: "2026-06-28", mes_numero: 6 },
    { semana_numero: 18, semana_key: "semana_18", mes: "Julio", dias: "29 al 5", fecha_inicio: "2026-06-29", fecha_fin: "2026-07-05", mes_numero: 6 },
    { semana_numero: 19, semana_key: "semana_19", mes: "Julio", dias: "6 al 12", fecha_inicio: "2026-07-06", fecha_fin: "2026-07-12", mes_numero: 7 },
    { semana_numero: 20, semana_key: "semana_20", mes: "Julio", dias: "13 al 19", fecha_inicio: "2026-07-13", fecha_fin: "2026-07-19", mes_numero: 7 }
  ];

  // Datos mock de asistencia
  const mockAttendanceRecords: AttendanceRecord[] = [
    { id: 1, semana: "semana_1", mes: "Marzo", dias: "2 al 8", estado: "asistió" },
    { id: 2, semana: "semana_2", mes: "Marzo", dias: "9 al 15", estado: "no asistió" },
    { id: 3, semana: "semana_3", mes: "Marzo", dias: "16 al 22", estado: "tutoría suspendida" },
    { id: 4, semana: "semana_4", mes: "Marzo", dias: "23 al 29", estado: "asistió" },
    { id: 5, semana: "semana_5", mes: "Marzo", dias: "30 al 5", estado: "vacaciones/feriado" }
  ];

  useEffect(() => {
    if (token) {
      fetchInitialData();
    }
  }, [token, user]);

  useEffect(() => {
    if (selectedStudent || selectedTutor) {
      fetchAttendanceRecords();
    }
  }, [selectedStudent, selectedTutor, token]);

  const fetchInitialData = async () => {
    try {
      // Usar datos mock del calendario
      setWeeks(mockWeeks);
      
      // Cargar estudiantes y tutores reales
      const promises = [
        fetchStudents().catch(() => setStudents([])),
        fetchTutors().catch(() => setTutors([]))
      ];

      if (user?.rol === 'admin') {
        promises.push(
          fetchSchools().catch(() => setSchools([]))
        );
      }

      await Promise.all(promises);
    } catch (error) {
      console.error('Error fetching initial data:', error);
      setStudents([]);
      setTutors([]);
      setSchools([]);
      setEquipos([]);
      setWeeks(mockWeeks); // Mantener calendario mock
      setAttendanceRecords([]);
    }
  };

  const fetchStudents = async () => {
    const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/estudiantes/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data)) {
        setStudents(data);
      } else {
        setStudents([]);
      }
    }
  };

  const fetchTutors = async () => {
    const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/tutores/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data)) {
        setTutors(data);
      } else {
        setTutors([]);
      }
    }
  };

  const fetchSchools = async () => {
    const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/schools/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data)) {
        setSchools(data);
      } else {
        setSchools([]);
      }
    }
  };

  const fetchAttendanceRecords = async () => {
    if (!selectedStudent && !selectedTutor) return;
    
    setLoading(true);
    try {
      // Simular carga de datos de asistencia
      setTimeout(() => {
        setAttendanceRecords(mockAttendanceRecords);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Error fetching attendance records:', error);
      setAttendanceRecords([]);
      setLoading(false);
    }
  };

  const updateAttendanceStatus = async (weekKey: string, estado: string | null, personId: number) => {
    try {
      // Simular actualización de asistencia
      const week = weeks.find(w => w.semana_key === weekKey);
      
      if (!week) return;
      
      // Actualizar el estado local (simulado)
      setAttendanceRecords(prev => {
        const existing = prev.find(r => r.semana === weekKey && r.id === personId);
        if (existing) {
          return prev.map(r => 
            r.semana === weekKey && r.id === personId ? { ...r, estado } : r
          );
        } else {
          return [...prev, {
            id: personId,
            semana: weekKey,
            mes: week.mes,
            dias: week.dias,
            estado
          }];
        }
      });
      
      console.log(`📝 Asistencia actualizada: ${weekKey} -> ${estado} para persona ${personId}`);
    } catch (error) {
      console.error('Error updating attendance:', error);
    }
  };

  const getAttendanceStatus = (weekKey: string, personId: number): string | null => {
    const record = attendanceRecords.find(r => r.semana === weekKey && r.id === personId);
    return record ? record.estado : null;
  };

  // Obtener meses únicos del calendario
  const getUniqueMonths = (): string[] => {
    const months = Array.from(new Set(weeks.map(week => week.mes)));
    return months.sort((a, b) => {
      const monthOrder = ['Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
      return monthOrder.indexOf(a) - monthOrder.indexOf(b);
    });
  };

  // Filtrar semanas por mes seleccionado
  const getFilteredWeeks = (): Week[] => {
    if (!selectedMonth) return weeks;
    return weeks.filter(week => week.mes === selectedMonth);
  };

  const getFilteredStudents = (): Student[] => {
    if (!Array.isArray(students)) return [];
    
    return students.filter(student => {
      if (user?.rol === 'admin') {
        if (selectedSchool && student.colegio_id !== selectedSchool) return false;
        if (selectedEquipo && student.equipo_id !== selectedEquipo) return false;
      }
      return true;
    });
  };

  const getFilteredTutors = (): Tutor[] => {
    if (!Array.isArray(tutors)) return [];
    
    return tutors.filter(tutor => {
      if (user?.rol === 'admin') {
        if (selectedSchool && tutor.colegio_id !== selectedSchool) return false;
        if (selectedEquipo && tutor.equipo_id !== selectedEquipo) return false;
      }
      return true;
    });
  };

  // Obtener personas según el tipo seleccionado
  const getFilteredPersons = (): (Student | Tutor)[] => {
    if (selectedPersonType === 'estudiante') {
      return getFilteredStudents();
    } else if (selectedPersonType === 'tutor') {
      return getFilteredTutors();
    }
    return [];
  };

  if (!token) {
    return <div className="container">Por favor, inicia sesión para acceder a la asistencia.</div>;
  }

  return (
    <div className="container">
      <h1>📅 Sistema de Asistencia 2026</h1>
      
      {/* Información de estado */}
      <div className="status-info">
        <div className="status-badge mock">🧪 MODO DEMO - Datos simulados</div>
        <p>Este es el frontend del sistema de asistencia con datos de prueba. Los cambios se guardan localmente.</p>
      </div>
      
      {/* Filtros y Selección */}
      <div className="filters">
        <h3>Configuración de Vista</h3>
        
        {/* Selección de tipo de persona */}
        <div className="filter-row">
          <div className="filter-group">
            <label>Tipo de Persona:</label>
            <select 
              value={selectedPersonType || ''} 
              onChange={(e) => {
                setSelectedPersonType(e.target.value as 'estudiante' | 'tutor' | null);
                setSelectedStudent(null);
                setSelectedTutor(null);
              }}
            >
              <option value="">Seleccionar tipo...</option>
              <option value="estudiante">Estudiantes</option>
              <option value="tutor">Tutores</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label>Mes:</label>
            <select 
              value={selectedMonth || ''} 
              onChange={(e) => setSelectedMonth(e.target.value || null)}
            >
              <option value="">Seleccionar mes...</option>
              {getUniqueMonths().map(month => (
                <option key={month} value={month}>{month}</option>
              ))}
            </select>
          </div>
        </div>
        
        {/* Filtros adicionales para admin */}
        {user?.rol === 'admin' && selectedPersonType && (
          <div className="filter-row">
            <div className="filter-group">
              <label>Colegio:</label>
              <select 
                value={selectedSchool || ''} 
                onChange={(e) => setSelectedSchool(e.target.value ? Number(e.target.value) : null)}
              >
                <option value="">Todos los colegios</option>
                {Array.isArray(schools) && schools.map(school => (
                  <option key={school.id} value={school.id}>{school.nombre}</option>
                ))}
              </select>
            </div>
            
            <div className="filter-group">
              <label>Equipo:</label>
              <select 
                value={selectedEquipo || ''} 
                onChange={(e) => setSelectedEquipo(e.target.value ? Number(e.target.value) : null)}
              >
                <option value="">Todos los equipos</option>
                {Array.isArray(equipos) && equipos.map(equipo => (
                  <option key={equipo.id} value={equipo.id}>{equipo.nombre}</option>
                ))}
              </select>
            </div>
          </div>
        )}
      </div>

      {/* Lista de Asistencia */}
      {selectedPersonType && selectedMonth && (
        <div className="attendance-calendar">
          <h3>
            Asistencia de {selectedPersonType === 'estudiante' ? 'Estudiantes' : 'Tutores'} - {selectedMonth}
          </h3>
          
          {loading ? (
            <div className="loading">Cargando registros de asistencia...</div>
          ) : (
            <div className="attendance-table-container">
              <table className="attendance-table">
                <thead>
                  <tr>
                    <th className="person-header">
                      {selectedPersonType === 'estudiante' ? 'Estudiante' : 'Tutor'}
                    </th>
                    {getFilteredWeeks().map(week => (
                      <th key={week.semana_key} className="week-header">
                        <div className="week-info">
                          <span className="week-number">S{week.semana_numero}</span>
                          <span className="week-dates">{week.dias}</span>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {getFilteredPersons().map(person => (
                    <tr key={person.id}>
                      <td className="person-cell">
                        <span className="person-name">
                          {person.nombre} {person.apellido}
                        </span>
                      </td>
                      {getFilteredWeeks().map(week => {
                        const currentStatus = getAttendanceStatus(week.semana_key, person.id);
                        const isEditing = editingWeek === week.semana_key && editingPerson === person.id;
                        
                        return (
                          <td key={`${person.id}-${week.semana_key}`} className="status-cell">
                            <div className="status-container">
                              {isEditing ? (
                                <div className="status-options">
                                  {attendanceStates.map(state => (
                                    <button
                                      key={state.key}
                                      className="status-option"
                                      style={{ backgroundColor: state.color }}
                                      onClick={() => {
                                        updateAttendanceStatus(week.semana_key, state.key, person.id);
                                        setEditingWeek(null);
                                        setEditingPerson(null);
                                      }}
                                    >
                                      {state.label}
                                    </button>
                                  ))}
                                  <button
                                    className="status-option clear"
                                    onClick={() => {
                                      updateAttendanceStatus(week.semana_key, null, person.id);
                                      setEditingWeek(null);
                                      setEditingPerson(null);
                                    }}
                                  >
                                    Limpiar
                                  </button>
                                  <button
                                    className="status-option cancel"
                                    onClick={() => {
                                      setEditingWeek(null);
                                      setEditingPerson(null);
                                    }}
                                  >
                                    Cancelar
                                  </button>
                                </div>
                              ) : (
                                <button
                                  className={`status-display ${currentStatus ? 'has-status' : 'no-status'}`}
                                  style={{ 
                                    backgroundColor: currentStatus 
                                      ? attendanceStates.find(s => s.key === currentStatus)?.color || '#6B7280'
                                      : '#f3f4f6',
                                    color: currentStatus ? 'white' : '#6B7280'
                                  }}
                                  onClick={() => {
                                    setEditingWeek(week.semana_key);
                                    setEditingPerson(person.id);
                                  }}
                                >
                                  {currentStatus 
                                    ? attendanceStates.find(s => s.key === currentStatus)?.label || 'Desconocido'
                                    : 'Sin estado'
                                  }
                                </button>
                              )}
                            </div>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Información adicional */}
      {(!selectedPersonType || !selectedMonth) && (
        <div className="info-section">
          <h3>📋 Instrucciones</h3>
          <ul>
            <li><strong>Paso 1:</strong> Selecciona el tipo de persona (Estudiantes o Tutores)</li>
            <li><strong>Paso 2:</strong> Selecciona el mes que quieres ver</li>
            {user?.rol === 'admin' && (
              <>
                <li><strong>Paso 3 (Admin):</strong> Opcionalmente filtra por colegio y/o equipo</li>
                <li><strong>Paso 4:</strong> Se mostrará la lista de personas con sus semanas de asistencia</li>
              </>
            )}
            {user?.rol !== 'admin' && (
              <li><strong>Paso 3:</strong> Se mostrará la lista de personas con sus semanas de asistencia</li>
            )}
            <li>Haz clic en cualquier celda de asistencia para cambiar el estado</li>
            <li>Los datos se guardan localmente (modo demo)</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default Asistencia;