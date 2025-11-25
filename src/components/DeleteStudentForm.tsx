import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Student {
  id: number;
  rut: string;
  nombre: string;
  apellido: string;
  curso: string;
  equipo_id: number;
}

interface DeleteStudentFormProps {
  students: Student[];
  onClose: () => void;
  onSuccess: () => void;
}

const DeleteStudentForm: React.FC<DeleteStudentFormProps> = ({ students, onClose, onSuccess }) => {
  const [selectedStudentId, setSelectedStudentId] = useState('');
  const [actionType, setActionType] = useState<'desercion' | 'eliminar' | ''>('');
  const [motivoDesercion, setMotivoDesercion] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { fetchWithAuth } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedStudentId) {
      setError('Por favor selecciona un estudiante');
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
      const response = await fetchWithAuth(`/estudiantes/${selectedStudentId}`, {
        method: 'DELETE',
        body: JSON.stringify({
          es_desercion: actionType === 'desercion',
          motivo_desercion: actionType === 'desercion' ? motivoDesercion.trim() : null
        }),
      });

      if (response.ok) {
        onSuccess();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al procesar la solicitud');
      }
    } catch (err) {
      setError('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="delete-form">
      <div className="form-group">
        <label htmlFor="student_id">Seleccionar Estudiante a Eliminar *</label>
        <select
          id="student_id"
          name="student_id"
          value={selectedStudentId}
          onChange={(e) => setSelectedStudentId(e.target.value)}
          required
        >
          <option value="">Seleccionar estudiante</option>
          {students.map((student) => (
            <option key={student.id} value={student.id}>
              {student.nombre} {student.apellido} - {student.curso} (RUT: {student.rut})
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>¿El alumno está mal creado o es un alumno que desertó? *</label>
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
            placeholder="Ingresa el motivo de deserción del estudiante..."
          />
        </div>
      )}

      {actionType === 'eliminar' && (
        <div className="warning-message">
          <p><strong>Advertencia:</strong> Esta acción eliminará permanentemente al estudiante 
          y todo su historial (asistencia, tickets, etc.) de la base de datos. Esta acción no se puede deshacer.</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      <div className="form-actions">
        <button type="button" onClick={onClose} className="btn btn-secondary">
          Cancelar
        </button>
        <button 
          type="submit" 
          disabled={loading || !selectedStudentId || !actionType || (actionType === 'desercion' && !motivoDesercion.trim())} 
          className="btn btn-danger"
        >
          {loading ? 'Procesando...' : actionType === 'desercion' ? 'Marcar como Desertor' : 'Eliminar Completamente'}
        </button>
      </div>
    </form>
  );
};

export default DeleteStudentForm;
