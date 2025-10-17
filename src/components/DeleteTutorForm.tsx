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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedTutorId) {
      setError('Por favor selecciona un tutor');
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
      });

      if (response.ok) {
        onSuccess();
        onClose();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al eliminar el tutor');
      }
    } catch (error) {
      console.error('Error al eliminar tutor:', error);
      setError('Error de conexión al eliminar el tutor');
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

          <div className="warning-message">
            <p><strong>Advertencia:</strong> Esta acción eliminará permanentemente al tutor 
            de la base de datos. Esta acción no se puede deshacer.</p>
          </div>

          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}

          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancelar
            </button>
            <button type="submit" className="btn btn-danger" disabled={loading}>
              {loading ? 'Eliminando...' : 'Eliminar Tutor'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DeleteTutorForm;
