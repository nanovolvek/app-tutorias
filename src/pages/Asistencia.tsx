import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useIsMobile } from '../hooks/useIsMobile';
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
  const { fetchWithAuth, user } = useAuth();
  
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
  const [expandedPersons, setExpandedPersons] = useState<Set<number>>(new Set());
  const [expandedWeeks, setExpandedWeeks] = useState<Set<string>>(new Set());
  const isMobile = useIsMobile();

  const togglePerson = (personId: number) => {
    setExpandedPersons(prev => {
      const newSet = new Set(prev);
      if (newSet.has(personId)) {
        newSet.delete(personId);
      } else {
        newSet.add(personId);
      }
      return newSet;
    });
  };

  const toggleWeek = (weekKey: string) => {
    setExpandedWeeks(prev => {
      const newSet = new Set(prev);
      if (newSet.has(weekKey)) {
        newSet.delete(weekKey);
      } else {
        newSet.add(weekKey);
      }
      return newSet;
    });
  };

  // Estados de asistencia
  const attendanceStates = [
    { key: 'asistió', label: 'Asistió', color: '#10B981' },
    { key: 'no asistió', label: 'No asistió', color: '#EF4444' },
    { key: 'tutoría suspendida', label: 'Suspendida', color: '#F59E0B' },
    { key: 'vacaciones/feriado', label: 'Vacaciones/Feriado', color: '#6B7280' }
  ];

  useEffect(() => {
    fetchInitialData();
  }, [user]);

  useEffect(() => {
    if (selectedPersonType && selectedMonth) {
      fetchAttendanceRecords();
    }
  }, [selectedPersonType, selectedMonth, selectedEquipo]);

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
    try {
      const response = await fetchWithAuth('/attendance-2026/calendar/weeks');
      
      if (response.ok) {
        const data = await response.json();
        if (data.weeks && Array.isArray(data.weeks)) {
          setWeeks(data.weeks);
        } else {
          setWeeks([]);
        }
      } else {
        setWeeks([]);
      }
    } catch (error) {
      console.error('Error fetching calendar:', error);
      setWeeks([]);
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await fetchWithAuth('/estudiantes/');
      if (response.ok) {
        const data = await response.json();
        if (Array.isArray(data)) {
          setStudents(data);
        } else {
          setStudents([]);
        }
      }
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  };

  const fetchTutors = async () => {
    try {
      const response = await fetchWithAuth('/tutores/');
      if (response.ok) {
        const data = await response.json();
        if (Array.isArray(data)) {
          setTutors(data);
        } else {
          setTutors([]);
        }
      }
    } catch (error) {
      console.error('Error fetching tutors:', error);
    }
  };

  const fetchEquipos = async () => {
    try {
      const response = await fetchWithAuth('/attendance-2026/equipos');
      
      if (response.ok) {
        const data = await response.json();
        if (Array.isArray(data)) {
          setEquipos(data);
        } else {
          setEquipos([]);
        }
      } else {
        console.error('Error fetching equipos:', response.status);
        setEquipos([]);
      }
    } catch (error) {
      console.error('Error fetching equipos:', error);
      setEquipos([]);
    }
  };

  const fetchAttendanceRecords = async () => {
    if (!selectedPersonType || !selectedMonth) return;
    
    setLoading(true);
    try {
      const personType = selectedPersonType === 'estudiante' ? 'students' : 'tutors';
      
      // Construir URL con parámetros
      const params = new URLSearchParams();
      params.append('month', selectedMonth);
      if (selectedEquipo) params.append('equipo_id', selectedEquipo.toString());
      
      const url = `/attendance-2026/${personType}?${params.toString()}`;
      
      const response = await fetchWithAuth(url);
      
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
        
        const response = await fetchWithAuth(`/attendance-2026/${personType}?${params.toString()}`, {
          method: 'DELETE',
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
      // Construir el body solo con los campos necesarios (sin undefined)
      const requestBody: any = {
        week_key: weekKey,
        status: estado
      };
      
      if (personType === 'students') {
        requestBody.student_id = personId;
      } else {
        requestBody.tutor_id = personId;
      }
      
      const response = await fetchWithAuth(`/attendance-2026/${personType}`, {
        method: 'POST',
        body: JSON.stringify(requestBody)
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
        let errorMessage = `Error ${response.status}: `;
        try {
          const errorData = await response.json();
          errorMessage += errorData.detail || 'Error desconocido';
          console.error('Error details:', errorData);
        } catch (e) {
          const errorText = await response.text();
          errorMessage += errorText || 'Error al procesar la respuesta';
          console.error('Error response text:', errorText);
        }
        alert(errorMessage);
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

  const handleExportExcel = async () => {
    try {
      const XLSX = await import('xlsx');
      
      // Obtener todos los meses disponibles
      const allMonths = getUniqueMonths();
      
      // Obtener datos de estudiantes con asistencia de todos los meses (sin filtros)
      const studentsData: any[] = [];
      for (const month of allMonths) {
        const params = new URLSearchParams();
        params.append('month', month);
        
        const response = await fetchWithAuth(`/attendance-2026/students?${params.toString()}`);
        if (response.ok) {
          const data = await response.json();
          studentsData.push(...data.students);
        }
      }
      
      // Obtener datos de tutores con asistencia de todos los meses (sin filtros)
      const tutorsData: any[] = [];
      for (const month of allMonths) {
        const params = new URLSearchParams();
        params.append('month', month);
        
        const response = await fetchWithAuth(`/attendance-2026/tutors?${params.toString()}`);
        if (response.ok) {
          const data = await response.json();
          tutorsData.push(...data.tutors);
        }
      }
      
      // Obtener información completa de estudiantes (con RUT, curso, etc.)
      const studentsResponse = await fetchWithAuth('/estudiantes/');
      const allStudents = studentsResponse.ok ? await studentsResponse.json() : [];
      
      // Obtener información completa de tutores (con email, etc.)
      const tutorsResponse = await fetchWithAuth('/tutores/');
      const allTutors = tutorsResponse.ok ? await tutorsResponse.json() : [];
      
      // Preparar datos de estudiantes para Excel
      const studentsExcelData: any[] = [
        ['RUT', 'Nombre', 'Apellido', 'Curso', 'Equipo', 'Colegio', 'Mes', 'Semana', 'Días', 'Estado']
      ];
      
      // Crear un mapa de estudiantes por ID para acceso rápido
      const studentsMap = new Map(allStudents.map((s: any) => [s.id, s]));
      
      studentsData.forEach((student: any) => {
        const studentInfo = studentsMap.get(student.id) as any;
        Object.entries(student.weekly_attendance).forEach(([weekKey, status]) => {
          const week = weeks.find(w => w.semana_key === weekKey);
          if (week) {
            studentsExcelData.push([
              studentInfo?.rut || 'N/A',
              student.nombre,
              student.apellido,
              studentInfo?.curso || 'N/A',
              student.equipo_nombre || 'Sin equipo',
              student.colegio_nombre || 'Sin colegio',
              week.mes,
              `S${week.semana_numero}`,
              week.dias,
              status as string
            ]);
          }
        });
      });
      
      // Preparar datos de tutores para Excel
      const tutorsExcelData: any[] = [
        ['Nombre', 'Apellido', 'Email', 'Equipo', 'Colegio', 'Mes', 'Semana', 'Días', 'Estado']
      ];
      
      // Crear un mapa de tutores por ID para acceso rápido
      const tutorsMap = new Map(allTutors.map((t: any) => [t.id, t]));
      
      tutorsData.forEach((tutor: any) => {
        const tutorInfo = tutorsMap.get(tutor.id) as any;
        Object.entries(tutor.weekly_attendance).forEach(([weekKey, status]) => {
          const week = weeks.find(w => w.semana_key === weekKey);
          if (week) {
            tutorsExcelData.push([
              tutor.nombre,
              tutor.apellido,
              tutorInfo?.email || tutor.email || 'N/A',
              tutor.equipo_nombre || 'Sin equipo',
              tutor.colegio_nombre || 'Sin colegio',
              week.mes,
              `S${week.semana_numero}`,
              week.dias,
              status as string
            ]);
          }
        });
      });
      
      // Crear libro de Excel con dos hojas
      const wb = XLSX.utils.book_new();
      
      // Hoja 1: Asistencia de Estudiantes
      const wsStudents = XLSX.utils.aoa_to_sheet(studentsExcelData);
      XLSX.utils.book_append_sheet(wb, wsStudents, 'Asistencia Estudiantes');
      
      // Hoja 2: Asistencia de Tutores
      const wsTutors = XLSX.utils.aoa_to_sheet(tutorsExcelData);
      XLSX.utils.book_append_sheet(wb, wsTutors, 'Asistencia Tutores');
      
      // Descargar archivo
      const fileName = `asistencia_${new Date().toISOString().split('T')[0]}.xlsx`;
      XLSX.writeFile(wb, fileName);
      
    } catch (error) {
      console.error('Error al exportar Excel:', error);
      alert('Error al exportar el archivo Excel. Por favor, intenta nuevamente.');
    }
  };

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
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3 style={{ margin: 0 }}>Configuración de Vista</h3>
          <button
            onClick={handleExportExcel}
            className="btn btn-success"
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#10B981',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '0.9rem',
              fontWeight: '500'
            }}
          >
            📊 Exportar Excel
          </button>
        </div>
        
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
            <>
              {isMobile ? (
                <div className="mobile-attendance-cards">
                  {getFilteredWeeks().map(week => {
                    const isExpanded = expandedWeeks.has(week.semana_key);
                    const personsInWeek = getFilteredPersons();
                    
                    return (
                      <div key={week.semana_key} className="mobile-attendance-card">
                        <div 
                          className="mobile-attendance-card-header"
                          onClick={() => toggleWeek(week.semana_key)}
                        >
                          <div className="mobile-attendance-card-title">
                            <div className="mobile-attendance-card-name">
                              Semana {week.semana_numero}
                            </div>
                            <div className="mobile-attendance-card-school">
                              {week.dias}
                            </div>
                          </div>
                          <div className="mobile-attendance-card-arrow">
                            {isExpanded ? '▼' : '▶'}
                          </div>
                        </div>
                        {isExpanded && (
                          <div className="mobile-attendance-card-content">
                            {personsInWeek.map(person => {
                              const personData = getPersonData(person.id);
                              const currentStatus = getAttendanceStatus(week.semana_key, person.id);
                              const isEditing = editingWeek === week.semana_key && editingPerson === person.id;
                              
                              return (
                                <div key={person.id} className="mobile-attendance-person">
                                  <div className="mobile-attendance-person-header">
                                    <div className="mobile-attendance-person-info">
                                      <div className="mobile-attendance-person-name">
                                        {person.nombre} {person.apellido}
                                      </div>
                                      <div className="mobile-attendance-person-school">
                                        {personData?.colegio_nombre || 'Sin colegio'}
                                      </div>
                                    </div>
                                  </div>
                                  <div className="mobile-attendance-person-status">
                                    {isEditing ? (
                                      <div className="mobile-status-options">
                                        {attendanceStates.map(state => (
                                          <button
                                            key={state.key}
                                            className="mobile-status-option"
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
                                          className="mobile-status-option clear"
                                          onClick={() => {
                                            updateAttendanceStatus(week.semana_key, null, person.id);
                                            setEditingWeek(null);
                                            setEditingPerson(null);
                                          }}
                                        >
                                          Sin estado
                                        </button>
                                        <button
                                          className="mobile-status-option cancel"
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
                                        className={`mobile-status-display ${currentStatus ? 'has-status' : 'no-status'}`}
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
                                </div>
                              );
                            })}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="attendance-table-container">
                  <table className="attendance-table">
                    <thead>
                      <tr>
                        <th className="person-header sticky-col-1">
                          {selectedPersonType === 'estudiante' ? 'Estudiante' : 'Tutor'}
                        </th>
                        <th className="school-header sticky-col-2">Colegio</th>
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
                            <td className="person-cell sticky-col-1">
                              <span className="person-name">
                                {person.nombre} {person.apellido}
                              </span>
                            </td>
                            <td className="school-cell sticky-col-2">
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
            </>
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