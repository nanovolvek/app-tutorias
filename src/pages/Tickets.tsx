import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Unidad {
  unidad_key: string;
  nombre: string;
  descripcion: string;
}

interface Modulo {
  modulo_key: string;
  nombre: string;
  descripcion: string;
}

interface Equipo {
  id: number;
  nombre: string;
  colegio_id: number;
  colegio_nombre?: string;
}

interface Student {
  id: number;
  nombre: string;
  apellido: string;
  equipo_id: number;
  colegio_nombre?: string;
  tickets: { [modulo_key: string]: string };
}

const Tickets: React.FC = () => {
  const { token, user } = useAuth();
  
  // Estados
  const [unidades, setUnidades] = useState<Unidad[]>([]);
  const [modulos, setModulos] = useState<Modulo[]>([]);
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedUnidad, setSelectedUnidad] = useState<string | null>(null);
  const [selectedEquipo, setSelectedEquipo] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [editingModulo, setEditingModulo] = useState<string | null>(null);
  const [editingStudent, setEditingStudent] = useState<number | null>(null);

  // Estados de tickets
  const ticketStates = [
    { key: 'vacío', label: 'Vacío', color: '#6B7280' },
    { key: '80%', label: '80%', color: '#F59E0B' },
    { key: '100%', label: '100%', color: '#10B981' }
  ];

  useEffect(() => {
    if (token) {
      fetchInitialData();
    }
  }, [token, user]);

  useEffect(() => {
    if (selectedUnidad) {
      fetchTicketsData();
    }
  }, [selectedUnidad, selectedEquipo, token]);

  const fetchInitialData = async () => {
    try {
      const promises = [
        fetchUnidades().catch(() => setUnidades([])),
        fetchEquipos().catch(() => setEquipos([]))
      ];

      await Promise.all(promises);
    } catch (error) {
      console.error('Error fetching initial data:', error);
      setUnidades([]);
      setEquipos([]);
    }
  };

  const fetchUnidades = async () => {
    const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
    console.log('📚 Fetching unidades from:', apiUrl);
    
    const response = await fetch(`${apiUrl}/tickets/unidades`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('📚 Unidades response status:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('📚 Unidades data received:', data.unidades.length, 'unidades');
      setUnidades(data.unidades);
    } else {
      console.error('❌ Error fetching unidades:', response.status);
    }
  };

  const fetchEquipos = async () => {
    const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/tickets/equipos`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('👥 Equipos data received:', data.length, 'equipos');
      setEquipos(data);
    }
  };

  const fetchTicketsData = async () => {
    if (!selectedUnidad) return;
    
    setLoading(true);
    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      
      // Construir URL con parámetros
      const params = new URLSearchParams();
      params.append('unidad', selectedUnidad);
      if (selectedEquipo) params.append('equipo_id', selectedEquipo.toString());
      
      const url = `${apiUrl}/tickets/students?${params.toString()}`;
      console.log('🎫 Fetching tickets from:', url);
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      console.log('🎫 Tickets response status:', response.status);
      
      if (response.status === 401) {
        console.error('❌ Token expirado o inválido. Por favor, vuelve a iniciar sesión.');
        return;
      }
      
      if (response.ok) {
        const data = await response.json();
        console.log('🎫 Tickets data received:', data.students.length, 'students');
        setStudents(data.students);
        setModulos(data.modulos);
      } else {
        console.error('❌ Error fetching tickets:', response.status);
        setStudents([]);
        setModulos([]);
      }
    } catch (error) {
      console.error('❌ Error fetching tickets:', error);
      setStudents([]);
      setModulos([]);
    } finally {
      setLoading(false);
    }
  };

  const updateTicketStatus = async (studentId: number, modulo: string, newStatus: string) => {
    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      
      const response = await fetch(`${apiUrl}/tickets/students`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: studentId,
          unidad: selectedUnidad,
          modulo: modulo,
          resultado: newStatus
        })
      });

      if (response.ok) {
        console.log('✅ Ticket updated successfully');
        // Actualizar el estado local
        setStudents(prevStudents => 
          prevStudents.map(student => 
            student.id === studentId 
              ? { ...student, tickets: { ...student.tickets, [modulo]: newStatus } }
              : student
          )
        );
      } else {
        console.error('❌ Error updating ticket:', response.status);
      }
    } catch (error) {
      console.error('❌ Error updating ticket:', error);
    }
  };

  const getTicketStatus = (modulo: string, studentId: number): string => {
    const student = students.find(s => s.id === studentId);
    return student?.tickets[modulo] || 'vacío';
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

  const getUnidadNombre = (): string => {
    const unidad = unidades.find(u => u.unidad_key === selectedUnidad);
    return unidad?.nombre || 'Unidad';
  };

  return (
    <div className="page-container">
      <div className="tickets-header">
        <h1 className="page-title">🎫 Sistema de Tickets</h1>
        <p className="page-description">
          Sistema de seguimiento de tickets por unidad y módulo. 
          Los tutores pueden gestionar los tickets de sus estudiantes.
        </p>
        <div className="status-indicator">
          ✅ CONECTADO - Datos reales de la base de datos
        </div>
      </div>

      <div className="filters-section">
        <h2>Configuración de Vista</h2>
        
        <div className="filter-row">
          <div className="filter-group">
            <label>Unidad:</label>
            <select 
              value={selectedUnidad || ''} 
              onChange={(e) => setSelectedUnidad(e.target.value || null)}
            >
              <option value="">Seleccionar unidad...</option>
              {unidades.map(unidad => (
                <option key={unidad.unidad_key} value={unidad.unidad_key}>
                  {unidad.nombre}
                </option>
              ))}
            </select>
          </div>

          {user?.rol === 'admin' && (
            <div className="filter-group">
              <label>Equipo:</label>
              <select 
                value={selectedEquipo || ''} 
                onChange={(e) => setSelectedEquipo(e.target.value ? parseInt(e.target.value) : null)}
              >
                <option value="">Todos los equipos</option>
                {Array.isArray(equipos) && equipos.map(equipo => (
                  <option key={equipo.id} value={equipo.id}>
                    {equipo.nombre} - {equipo.colegio_nombre}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      </div>

      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando datos de tickets...</p>
        </div>
      )}

      {!loading && selectedUnidad && (
        <div className="tickets-content">
          <h2>Tickets de Estudiantes - {getUnidadNombre()}</h2>
          
          {getFilteredStudents().length === 0 ? (
            <div className="no-data">
              <p>No hay estudiantes disponibles para mostrar.</p>
            </div>
          ) : (
            <div className="tickets-table-container">
              <table className="tickets-table">
                <thead>
                  <tr>
                    <th className="student-header">
                      Estudiante
                    </th>
                    {user?.rol === 'admin' && (
                      <th className="school-header">Colegio</th>
                    )}
                    {modulos.map(modulo => (
                      <th key={modulo.modulo_key} className="modulo-header">
                        <div className="modulo-title">{modulo.nombre}</div>
                        <div className="modulo-desc">{modulo.descripcion}</div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {getFilteredStudents().map(student => (
                    <tr key={student.id}>
                      <td className="student-cell">
                        <span className="student-name">
                          {student.nombre} {student.apellido}
                        </span>
                      </td>
                      {user?.rol === 'admin' && (
                        <td className="school-cell">
                          <span className="school-name">
                            {student.colegio_nombre || 'Sin colegio'}
                          </span>
                        </td>
                      )}
                      {modulos.map(modulo => {
                        const currentStatus = getTicketStatus(modulo.modulo_key, student.id);
                        const isEditing = editingModulo === modulo.modulo_key && editingStudent === student.id;
                        
                        return (
                          <td key={modulo.modulo_key} className="ticket-cell">
                            <div className="ticket-container">
                              {isEditing ? (
                                <div className="ticket-editor">
                                  {ticketStates.map(state => (
                                    <button
                                      key={state.key}
                                      className={`ticket-option ${currentStatus === state.key ? 'active' : ''}`}
                                      style={{ backgroundColor: state.color }}
                                      onClick={() => {
                                        updateTicketStatus(student.id, modulo.modulo_key, state.key);
                                        setEditingModulo(null);
                                        setEditingStudent(null);
                                      }}
                                    >
                                      {state.label}
                                    </button>
                                  ))}
                                  <button
                                    className="ticket-cancel"
                                    onClick={() => {
                                      setEditingModulo(null);
                                      setEditingStudent(null);
                                    }}
                                  >
                                    ✕
                                  </button>
                                </div>
                              ) : (
                                <button
                                  className={`ticket-display ${currentStatus}`}
                                  style={{ 
                                    backgroundColor: ticketStates.find(s => s.key === currentStatus)?.color || '#6B7280'
                                  }}
                                  onClick={() => {
                                    setEditingModulo(modulo.modulo_key);
                                    setEditingStudent(student.id);
                                  }}
                                >
                                  {ticketStates.find(s => s.key === currentStatus)?.label || 'Vacío'}
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

      {!selectedUnidad && !loading && (
        <div className="instructions">
          <h3>📋 Instrucciones</h3>
          <ol>
            <li>Selecciona la unidad que quieres ver</li>
            <li>{user?.rol === 'admin' ? 'Opcionalmente filtra por equipo' : 'Se mostrarán los estudiantes de tu equipo'}</li>
            <li>Se mostrará la lista de estudiantes con sus módulos de tickets</li>
            <li>Haz clic en cualquier celda de ticket para cambiar el resultado</li>
            <li>Los datos se guardan en la base de datos en tiempo real</li>
          </ol>
        </div>
      )}

      <style dangerouslySetInnerHTML={{
        __html: `
          .tickets-header {
            text-align: center;
            margin-bottom: 2rem;
          }

          .page-title {
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 1rem;
            font-weight: 700;
          }

          .page-description {
            font-size: 1.1rem;
            color: #718096;
            line-height: 1.6;
            max-width: 600px;
            margin: 0 auto 1rem;
          }

          .status-indicator {
            background: linear-gradient(135deg, #10B981, #059669);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 2rem;
          }

          .filters-section {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
          }

          .filters-section h2 {
            color: #2d3748;
            margin-bottom: 1rem;
            font-size: 1.3rem;
          }

          .filter-row {
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
            align-items: end;
          }

          .filter-group {
            display: flex;
            flex-direction: column;
            min-width: 200px;
          }

          .filter-group label {
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 0.5rem;
          }

          .filter-group select {
            padding: 0.75rem;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            background: white;
            transition: border-color 0.3s ease;
          }

          .filter-group select:focus {
            outline: none;
            border-color: #667eea;
          }

          .loading-container {
            text-align: center;
            padding: 3rem;
          }

          .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #e2e8f0;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
          }

          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }

          .tickets-content h2 {
            color: #2d3748;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
          }

          .no-data {
            text-align: center;
            padding: 3rem;
            color: #718096;
            background: #f7fafc;
            border-radius: 15px;
          }

          .tickets-table-container {
            overflow-x: auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
          }

          .tickets-table {
            width: 100%;
            border-collapse: collapse;
            min-width: 600px;
          }

          .tickets-table th {
            background: #f8fafc;
            padding: 1rem;
            text-align: center;
            font-weight: 600;
            color: #2d3748;
            border-bottom: 2px solid #e2e8f0;
          }

          .student-header {
            min-width: 150px;
          }

          .school-header {
            min-width: 120px;
          }

          .modulo-header {
            min-width: 100px;
          }

          .modulo-title {
            font-weight: 600;
            margin-bottom: 0.25rem;
          }

          .modulo-desc {
            font-size: 0.8rem;
            color: #718096;
            font-weight: normal;
          }

          .tickets-table td {
            padding: 1rem;
            text-align: center;
            border-bottom: 1px solid #e2e8f0;
            vertical-align: middle;
          }

          .student-cell {
            text-align: left;
          }

          .student-name {
            font-weight: 600;
            color: #2d3748;
          }

          .school-cell {
            text-align: left;
          }

          .school-name {
            color: #718096;
            font-size: 0.9rem;
          }

          .ticket-cell {
            padding: 0.5rem;
          }

          .ticket-container {
            display: flex;
            justify-content: center;
            align-items: center;
          }

          .ticket-display {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 20px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 60px;
          }

          .ticket-display:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
          }

          .ticket-editor {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            align-items: center;
          }

          .ticket-option {
            padding: 0.4rem 0.8rem;
            border: none;
            border-radius: 15px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            min-width: 50px;
          }

          .ticket-option:hover {
            transform: scale(1.05);
          }

          .ticket-option.active {
            border: 2px solid white;
            box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.2);
          }

          .ticket-cancel {
            padding: 0.3rem 0.6rem;
            border: none;
            border-radius: 50%;
            background: #ef4444;
            color: white;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.3s ease;
          }

          .ticket-cancel:hover {
            background: #dc2626;
            transform: scale(1.1);
          }

          .instructions {
            background: #f0f9ff;
            border: 1px solid #0ea5e9;
            border-radius: 15px;
            padding: 2rem;
            margin-top: 2rem;
          }

          .instructions h3 {
            color: #0369a1;
            margin-bottom: 1rem;
          }

          .instructions ol {
            color: #0c4a6e;
            line-height: 1.6;
          }

          .instructions li {
            margin-bottom: 0.5rem;
          }

          @media (max-width: 768px) {
            .filter-row {
              flex-direction: column;
              gap: 1rem;
            }

            .filter-group {
              min-width: 100%;
            }

            .tickets-table-container {
              font-size: 0.9rem;
            }

            .tickets-table th,
            .tickets-table td {
              padding: 0.5rem;
            }

            .modulo-title {
              font-size: 0.9rem;
            }

            .modulo-desc {
              font-size: 0.7rem;
            }
          }
        `
      }} />
    </div>
  );
};

export default Tickets;
