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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { token } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedStudentId) {
      setError('Por favor selecciona un estudiante');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/estudiantes/${selectedStudentId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        onSuccess();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al eliminar el estudiante');
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

      <div className="warning-message">
        <p><strong>Advertencia:</strong> Esta acción eliminará permanentemente al estudiante 
        de la base de datos. Esta acción no se puede deshacer.</p>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      <div className="form-actions">
        <button type="button" onClick={onClose} className="btn btn-secondary">
          Cancelar
        </button>
        <button type="submit" disabled={loading || !selectedStudentId} className="btn btn-danger">
          {loading ? 'Eliminando...' : 'Eliminar Estudiante'}
        </button>
      </div>
    </form>
  );
};

export default DeleteStudentForm;
