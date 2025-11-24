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

interface Equipo {
  id: number;
  nombre: string;
  colegio_nombre?: string;
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
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [selectedEquipo, setSelectedEquipo] = useState<number | null>(null);
  const [selectedMonth, setSelectedMonth] = useState<string | null>(null);
  const [selectedPersonType, setSelectedPersonType] = useState<'estudiante' | 'tutor' | null>(null);
  const [attendanceRecords, setAttendanceRecords] = useState<AttendanceRecord[]>([]);
  const [personsData, setPersonsData] = useState<any[]>([]);
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

  useEffect(() => {
    if (token) {
      fetchInitialData();
    }
  }, [token, user]);

  useEffect(() => {
    if (selectedPersonType && selectedMonth) {
      fetchAttendanceRecords();
    }
  }, [selectedPersonType, selectedMonth, selectedEquipo, token]);

  const fetchInitialData = async () => {
    try {
      // Cargar calendario desde API
      await fetchCalendar();
      
      // Cargar estudiantes y tutores reales
      const promises = [
        fetchStudents().catch(() => setStudents([])),
        fetchTutors().catch(() => setTutors([]))
      ];

      if (user?.rol === 'admin') {
        promises.push(
          fetchEquipos().catch(() => setEquipos([]))
        );
      }

      await Promise.all(promises);
    } catch (error) {
      console.error('Error fetching initial data:', error);
      setStudents([]);
      setTutors([]);
      setEquipos([]);
      setWeeks([]);
      setAttendanceRecords([]);
    }
  };

  const fetchCalendar = async () => {
    const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
    console.log('🔍 Fetching calendar from:', apiUrl);
    
    const response = await fetch(`${apiUrl}/attendance-2026/calendar/weeks`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('📅 Calendar response status:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('📅 Calendar data received:', data);
      if (data.weeks && Array.isArray(data.weeks)) {
        setWeeks(data.weeks);
        console.log('✅ Calendar weeks set:', data.weeks.length);
      } else {
        setWeeks([]); // Fallback a array vacío
        console.log('⚠️ Using mock weeks fallback');
      }
    } else {
      console.error('❌ Error fetching calendar:', response.status);
      setWeeks([]); // Fallback a array vacío
    }
  };

  const fetchStudents = async () => {
    const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
    console.log('👥 Fetching students from:', apiUrl);
    
    const response = await fetch(`${apiUrl}/estudiantes/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('👥 Students response status:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('👥 Students data received:', data.length, 'students');
      if (Array.isArray(data)) {
        setStudents(data);
      } else {
        setStudents([]);
      }
    } else {
      console.error('❌ Error fetching students:', response.status);
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

  const fetchEquipos = async () => {
    const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
    console.log('👥 Fetching equipos from:', apiUrl);
    
    const response = await fetch(`${apiUrl}/attendance-2026/equipos`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('👥 Equipos response status:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('👥 Equipos data received:', data.length, 'equipos');
      if (Array.isArray(data)) {
        setEquipos(data);
      } else {
        setEquipos([]);
      }
    } else {
      console.error('❌ Error fetching equipos:', response.status);
    }
  };

  const fetchAttendanceRecords = async () => {
    if (!selectedPersonType || !selectedMonth) return;
    
    setLoading(true);
    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const personType = selectedPersonType === 'estudiante' ? 'students' : 'tutors';
      
      // Construir URL con parámetros
      const params = new URLSearchParams();
      params.append('month', selectedMonth);
      if (selectedEquipo) params.append('equipo_id', selectedEquipo.toString());
      
      const url = `${apiUrl}/attendance-2026/${personType}?${params.toString()}`;
      console.log('📊 Fetching attendance from:', url);
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      console.log('📊 Attendance response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        const persons = personType === 'students' ? data.students : data.tutors;
        console.log('📊 Attendance data received:', persons.length, 'persons');
        
        // Convertir datos de la API al formato esperado por el frontend
        const records: AttendanceRecord[] = [];
        persons.forEach((person: any) => {
          console.log('👤 Processing person:', person.nombre, person.apellido, 'Colegio:', person.colegio_nombre);
          Object.entries(person.weekly_attendance).forEach(([week, status]) => {
            const weekData = weeks.find(w => w.semana_key === week);
            if (weekData) {
              records.push({
                id: person.id,
                semana: week,
                mes: weekData.mes,
                dias: weekData.dias,
                estado: status as string
              });
            }
          });
        });
        
        console.log('📊 Processed records:', records.length);
        setAttendanceRecords(records);
        setPersonsData(persons); // Guardar datos de las personas
      } else {
        console.error('❌ Error fetching attendance records:', response.status);
        setAttendanceRecords([]);
        setPersonsData([]);
      }
    } catch (error) {
      console.error('❌ Error fetching attendance records:', error);
      setAttendanceRecords([]);
      setPersonsData([]);
    } finally {
      setLoading(false);
    }
  };

  const updateAttendanceStatus = async (weekKey: string, estado: string | null, personId: number) => {
    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const personType = selectedPersonType === 'estudiante' ? 'students' : 'tutors';
      
      if (estado === null) {
        // Eliminar registro de asistencia usando DELETE
        const params = new URLSearchParams();
        if (personType === 'students') {
          params.append('student_id', personId.toString());
        } else {
          params.append('tutor_id', personId.toString());
        }
        params.append('week_key', weekKey);
        
        const response = await fetch(`${apiUrl}/attendance-2026/${personType}?${params.toString()}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log(`✅ Registro de asistencia eliminado:`, data);
          
          // Eliminar el registro del estado local
          setAttendanceRecords(prev => 
            prev.filter(r => !(r.semana === weekKey && r.id === personId))
          );
          
          // Actualizar los datos de las personas para reflejar el cambio
          setPersonsData(prev => prev.map(person => {
            if (person.id === personId) {
              const updatedWeeklyAttendance = { ...person.weekly_attendance };
              delete updatedWeeklyAttendance[weekKey];
              return { ...person, weekly_attendance: updatedWeeklyAttendance };
            }
            return person;
          }));
        } else {
          console.error('Error deleting attendance:', response.status);
          const errorData = await response.json().catch(() => ({}));
          console.error('Error details:', errorData);
        }
        return;
      }
      
      // Crear o actualizar registro de asistencia
      const response = await fetch(`${apiUrl}/attendance-2026/${personType}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: personType === 'students' ? personId : undefined,
          tutor_id: personType === 'tutors' ? personId : undefined,
          week_key: weekKey,
          status: estado
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log(`✅ Asistencia actualizada:`, data);
        
        // Actualizar el estado local
        setAttendanceRecords(prev => {
          const existing = prev.find(r => r.semana === weekKey && r.id === personId);
          if (existing) {
            return prev.map(r => 
              r.semana === weekKey && r.id === personId ? { ...r, estado } : r
            );
          } else {
            const week = weeks.find(w => w.semana_key === weekKey);
            return [...prev, {
              id: personId,
              semana: weekKey,
              mes: week?.mes || '',
              dias: week?.dias || '',
              estado
            }];
          }
        });
        
        // Actualizar los datos de las personas
        setPersonsData(prev => prev.map(person => {
          if (person.id === personId) {
            return {
              ...person,
              weekly_attendance: {
                ...person.weekly_attendance,
                [weekKey]: estado
              }
            };
          }
          return person;
        }));
      } else {
        console.error('Error updating attendance:', response.status);
        const errorData = await response.json();
        console.error('Error details:', errorData);
      }
    } catch (error) {
      console.error('Error updating attendance:', error);
    }
  };

  const getPersonData = (personId: number): any => {
    return personsData.find(person => person.id === personId);
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
        if (selectedEquipo && student.equipo_id !== selectedEquipo) return false;
      }
      return true;
    });
  };

  const getFilteredTutors = (): Tutor[] => {
    if (!Array.isArray(tutors)) return [];
    
    return tutors.filter(tutor => {
      if (user?.rol === 'admin') {
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
        <div className="status-badge real">✅ CONECTADO - Datos reales de la base de datos</div>
        <p>Este es el sistema de asistencia conectado a la API. Los cambios se guardan en la base de datos.</p>
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
              <label>Equipo:</label>
              <select 
                value={selectedEquipo || ''} 
                onChange={(e) => setSelectedEquipo(e.target.value ? Number(e.target.value) : null)}
              >
                <option value="">Todos los equipos</option>
                {Array.isArray(equipos) && equipos.map(equipo => (
                  <option key={equipo.id} value={equipo.id}>{equipo.nombre} - {equipo.colegio_nombre}</option>
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
                    <th className="school-header">Colegio</th>
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
                  {getFilteredPersons().map(person => {
                    const personData = getPersonData(person.id);
                    return (
                      <tr key={person.id}>
                        <td className="person-cell">
                          <span className="person-name">
                            {person.nombre} {person.apellido}
                          </span>
                        </td>
                        <td className="school-cell">
                          <span className="school-name">
                            {personData?.colegio_nombre || 'Sin colegio'}
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
                                    Sin estado
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
                    );
                  })}
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
            <li>Los datos se guardan en la base de datos en tiempo real</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default Asistencia;