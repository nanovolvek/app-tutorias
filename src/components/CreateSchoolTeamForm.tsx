import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Colegio {
  id: number;
  nombre?: string;
  name?: string; // Por si viene con alias
  comuna: string;
}

interface CreateSchoolTeamFormProps {
  onSuccess: () => void;
  onClose: () => void;
}

const CreateSchoolTeamForm: React.FC<CreateSchoolTeamFormProps> = ({ onSuccess, onClose }) => {
  const { fetchWithAuth } = useAuth();
  const [activeTab, setActiveTab] = useState<'school' | 'team'>('school');
  const [colegios, setColegios] = useState<Colegio[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Formulario de colegio
  const [schoolNombre, setSchoolNombre] = useState('');
  const [schoolComuna, setSchoolComuna] = useState('');

  // Formulario de equipo
  const [selectedColegioId, setSelectedColegioId] = useState<number | ''>('');
  const [teamNombre, setTeamNombre] = useState('');
  const [teamDescripcion, setTeamDescripcion] = useState('');

  useEffect(() => {
    fetchColegios();
  }, []);

  const fetchColegios = async () => {
    try {
      const response = await fetchWithAuth('/schools/');
      if (response.ok) {
        const data = await response.json();
        console.log('Colegios recibidos:', data); // Debug
        setColegios(data);
      } else {
        console.error('Error al cargar colegios:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error al cargar colegios:', error);
    }
  };

  const handleCreateSchool = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!schoolNombre.trim() || !schoolComuna.trim()) {
      setError('Por favor completa todos los campos requeridos');
      return;
    }

    setLoading(true);
    setError('');
    setSuccessMessage('');

    try {
      const response = await fetchWithAuth('/schools/', {
        method: 'POST',
        body: JSON.stringify({
          nombre: schoolNombre.trim(),
          comuna: schoolComuna.trim()
        })
      });

      if (response.ok) {
        const newSchool = await response.json();
        setSuccessMessage(`Colegio "${newSchool.nombre}" creado exitosamente`);
        setSchoolNombre('');
        setSchoolComuna('');
        await fetchColegios();
        // Opcional: seleccionar el colegio recién creado si estamos en la pestaña de equipo
        if (activeTab === 'team') {
          setSelectedColegioId(newSchool.id);
        }
        onSuccess(); // Recargar datos en el Dashboard
        setTimeout(() => {
          setSuccessMessage('');
        }, 2000);
      } else {
        const data = await response.json();
        setError(data.detail || 'Error al crear el colegio');
      }
    } catch (error: any) {
      console.error('Error al crear colegio:', error);
      setError(error.message || 'Error de conexión al crear el colegio');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTeam = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teamNombre.trim()) {
      setError('El nombre del equipo es requerido');
      return;
    }

    setLoading(true);
    setError('');
    setSuccessMessage('');

    try {
      const response = await fetchWithAuth('/equipos/', {
        method: 'POST',
        body: JSON.stringify({
          nombre: teamNombre.trim(),
          descripcion: teamDescripcion.trim() || null,
          colegio_id: selectedColegioId || null
        })
      });

      if (response.ok) {
        const newTeam = await response.json();
        setSuccessMessage(`Equipo "${newTeam.nombre}" creado exitosamente`);
        setTeamNombre('');
        setTeamDescripcion('');
        setSelectedColegioId('');
        onSuccess(); // Recargar datos en el Dashboard
        setTimeout(() => {
          setSuccessMessage('');
          // No cerrar automáticamente, permitir crear más
        }, 2000);
      } else {
        const data = await response.json();
        setError(data.detail || 'Error al crear el equipo');
      }
    } catch (error: any) {
      console.error('Error al crear equipo:', error);
      setError(error.message || 'Error de conexión al crear el equipo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px' }}>
        <div className="modal-header">
          <h2>Crear Colegio y Equipo</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {/* Pestañas para seleccionar qué crear */}
          <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', borderBottom: '2px solid #e5e7eb' }}>
            <button
              type="button"
              onClick={() => {
                setActiveTab('school');
                setError('');
                setSuccessMessage('');
              }}
              style={{
                padding: '12px 24px',
                border: 'none',
                borderBottom: activeTab === 'school' ? '3px solid #3b82f6' : '3px solid transparent',
                backgroundColor: 'transparent',
                color: activeTab === 'school' ? '#3b82f6' : '#6b7280',
                fontWeight: activeTab === 'school' ? '600' : '400',
                fontSize: '1rem',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              Crear Colegio
            </button>
            <button
              type="button"
              onClick={() => {
                setActiveTab('team');
                setError('');
                setSuccessMessage('');
              }}
              style={{
                padding: '12px 24px',
                border: 'none',
                borderBottom: activeTab === 'team' ? '3px solid #3b82f6' : '3px solid transparent',
                backgroundColor: 'transparent',
                color: activeTab === 'team' ? '#3b82f6' : '#6b7280',
                fontWeight: activeTab === 'team' ? '600' : '400',
                fontSize: '1rem',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              Crear Equipo
            </button>
          </div>

          {error && (
            <div style={{ padding: '12px', backgroundColor: '#fee2e2', color: '#991b1b', borderRadius: '4px', marginBottom: '16px' }}>
              {error}
            </div>
          )}

          {successMessage && (
            <div style={{ padding: '12px', backgroundColor: '#dcfce7', color: '#166534', borderRadius: '4px', marginBottom: '16px' }}>
              {successMessage}
            </div>
          )}

          {activeTab === 'school' ? (
            <form onSubmit={handleCreateSchool}>
              <div className="form-group">
                <label htmlFor="school-nombre">Nombre del Colegio *</label>
                <input
                  id="school-nombre"
                  type="text"
                  value={schoolNombre}
                  onChange={(e) => setSchoolNombre(e.target.value)}
                  disabled={loading}
                  required
                  placeholder="Ej: Colegio San Patricio"
                />
              </div>

              <div className="form-group">
                <label htmlFor="school-comuna">Comuna *</label>
                <input
                  id="school-comuna"
                  type="text"
                  value={schoolComuna}
                  onChange={(e) => setSchoolComuna(e.target.value)}
                  disabled={loading}
                  required
                  placeholder="Ej: Santiago"
                />
              </div>

              <div className="form-actions">
                <button
                  type="button"
                  onClick={onClose}
                  disabled={loading}
                  className="btn btn-secondary"
                >
                  Cerrar
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="btn btn-primary"
                >
                  {loading ? 'Creando...' : 'Crear Colegio'}
                </button>
              </div>
            </form>
          ) : (
            <form onSubmit={handleCreateTeam}>
              <div className="form-group">
                <label htmlFor="team-colegio">Colegio (opcional)</label>
                <select
                  id="team-colegio"
                  value={selectedColegioId}
                  onChange={(e) => setSelectedColegioId(e.target.value ? parseInt(e.target.value) : '')}
                  disabled={loading}
                  style={{ width: '100%', padding: '8px', border: '1px solid #d1d5db', borderRadius: '4px' }}
                >
                  <option value="">Sin colegio</option>
                  {colegios.length > 0 ? (
                    colegios.map((colegio) => {
                      const nombre = colegio.nombre || colegio.name || 'Sin nombre';
                      return (
                        <option key={colegio.id} value={colegio.id}>
                          {nombre} - {colegio.comuna}
                        </option>
                      );
                    })
                  ) : (
                    <option disabled>No hay colegios disponibles</option>
                  )}
                </select>
                <small style={{ color: '#6b7280', fontSize: '0.85rem', marginTop: '4px', display: 'block' }}>
                  Puedes crear el equipo sin asignarlo a un colegio ahora
                </small>
              </div>

              <div className="form-group">
                <label htmlFor="team-nombre">Nombre del Equipo *</label>
                <input
                  id="team-nombre"
                  type="text"
                  value={teamNombre}
                  onChange={(e) => setTeamNombre(e.target.value)}
                  disabled={loading}
                  required
                  placeholder="Ej: A, B, C, Equipo 1, etc."
                />
                <small style={{ color: '#6b7280', fontSize: '0.85rem', marginTop: '4px', display: 'block' }}>
                  El nombre debe ser único
                </small>
              </div>

              <div className="form-group">
                <label htmlFor="team-descripcion">Descripción (opcional)</label>
                <textarea
                  id="team-descripcion"
                  value={teamDescripcion}
                  onChange={(e) => setTeamDescripcion(e.target.value)}
                  disabled={loading}
                  placeholder="Descripción del equipo..."
                  rows={3}
                />
              </div>

              <div className="form-actions">
                <button
                  type="button"
                  onClick={onClose}
                  disabled={loading}
                  className="btn btn-secondary"
                >
                  Cerrar
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="btn btn-primary"
                >
                  {loading ? 'Creando...' : 'Crear Equipo'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default CreateSchoolTeamForm;

