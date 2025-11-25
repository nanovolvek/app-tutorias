import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Tutor {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  equipo?: {
    nombre: string;
  };
}

interface DeleteTutorFormProps {
  onSuccess: () => void;
  onClose: () => void;
  tutores: Tutor[];
}

const DeleteTutorForm: React.FC<DeleteTutorFormProps> = ({ onSuccess, onClose, tutores }) => {
  const { token } = useAuth();
  const [selectedTutorId, setSelectedTutorId] = useState('');
  const [actionType, setActionType] = useState<'desercion' | 'eliminar' | ''>('');
  const [motivoDesercion, setMotivoDesercion] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedTutorId) {
      setError('Por favor selecciona un tutor');
      return;
    }

    if (!actionType) {
      setError('Por favor selecciona una opción');
      return;
    }

    if (actionType === 'desercion' && !motivoDesercion.trim()) {
      setError('Por favor ingresa el motivo de deserción');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/tutores/${selectedTutorId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          es_desercion: actionType === 'desercion',
          motivo_desercion: actionType === 'desercion' ? motivoDesercion.trim() : null
        }),
      });

      if (response.ok) {
        onSuccess();
        onClose();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al procesar la solicitud');
      }
    } catch (error) {
      console.error('Error al procesar tutor:', error);
      setError('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Eliminar Tutor</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        <form className="delete-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="tutor_id">Seleccionar Tutor *</label>
            <select
              id="tutor_id"
              value={selectedTutorId}
              onChange={(e) => setSelectedTutorId(e.target.value)}
              required
            >
              <option value="">Seleccionar tutor a eliminar</option>
              {tutores.map(tutor => (
                <option key={tutor.id} value={tutor.id}>
                  {tutor.nombre} {tutor.apellido} - {tutor.equipo?.nombre || 'Sin equipo'}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>¿El tutor está mal creado o es un tutor que desertó? *</label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '8px' }}>
              <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="actionType"
                  value="desercion"
                  checked={actionType === 'desercion'}
                  onChange={(e) => setActionType(e.target.value as 'desercion')}
                  style={{ marginRight: '8px' }}
                />
                <span>Desertó</span>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="actionType"
                  value="eliminar"
                  checked={actionType === 'eliminar'}
                  onChange={(e) => setActionType(e.target.value as 'eliminar')}
                  style={{ marginRight: '8px' }}
                />
                <span>Está mal creado (eliminar completamente)</span>
              </label>
            </div>
          </div>

          {actionType === 'desercion' && (
            <div className="form-group">
              <label htmlFor="motivo_desercion">Motivo de Deserción *</label>
              <textarea
                id="motivo_desercion"
                name="motivo_desercion"
                value={motivoDesercion}
                onChange={(e) => setMotivoDesercion(e.target.value)}
                required
                rows={3}
                placeholder="Ingresa el motivo de deserción del tutor..."
              />
            </div>
          )}

          {actionType === 'eliminar' && (
            <div className="warning-message">
              <p><strong>Advertencia:</strong> Esta acción eliminará permanentemente al tutor 
              y todo su historial (asistencia, etc.) de la base de datos. Esta acción no se puede deshacer.</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}

          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancelar
            </button>
            <button 
              type="submit" 
              className="btn btn-danger" 
              disabled={loading || !selectedTutorId || !actionType || (actionType === 'desercion' && !motivoDesercion.trim())}
            >
              {loading ? 'Procesando...' : actionType === 'desercion' ? 'Marcar como Desertor' : 'Eliminar Completamente'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DeleteTutorForm;
