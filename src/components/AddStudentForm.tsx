import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

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

interface AddStudentFormProps {
  onClose: () => void;
  onSuccess: () => void;
  user: any;
}

const AddStudentForm: React.FC<AddStudentFormProps> = ({ onClose, onSuccess, user }) => {
  const [formData, setFormData] = useState({
    rut: '',
    nombre: '',
    apellido: '',
    curso: '',
    equipo_id: user?.rol === 'tutor' ? user.equipo_id : '',
    nombre_apoderado: '',
    contacto_apoderado: '',
    observaciones: ''
  });
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { token } = useAuth();

  useEffect(() => {
    if (user?.rol === 'admin') {
      fetchEquipos();
    }
  }, [user]);

  const fetchEquipos = async () => {
    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/equipos/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setEquipos(data);
      }
    } catch (err) {
      console.error('Error al cargar equipos:', err);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/estudiantes/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          equipo_id: parseInt(formData.equipo_id.toString())
        }),
      });

      if (response.ok) {
        onSuccess();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al crear el estudiante');
      }
    } catch (err) {
      setError('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="student-form">
      <div className="form-group">
        <label htmlFor="rut">RUT *</label>
        <input
          type="text"
          id="rut"
          name="rut"
          value={formData.rut}
          onChange={handleInputChange}
          required
          placeholder="12.345.678-9"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="nombre">Nombre *</label>
          <input
            type="text"
            id="nombre"
            name="nombre"
            value={formData.nombre}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="apellido">Apellido *</label>
          <input
            type="text"
            id="apellido"
            name="apellido"
            value={formData.apellido}
            onChange={handleInputChange}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="curso">Curso *</label>
        <input
          type="text"
          id="curso"
          name="curso"
          value={formData.curso}
          onChange={handleInputChange}
          required
          placeholder="3° Básico, 1° Medio, etc."
        />
      </div>

      {user?.rol === 'admin' ? (
        <div className="form-group">
          <label htmlFor="equipo_id">Equipo *</label>
          <select
            id="equipo_id"
            name="equipo_id"
            value={formData.equipo_id}
            onChange={handleInputChange}
            required
          >
            <option value="">Seleccionar equipo</option>
            {equipos.map((equipo) => (
              <option key={equipo.id} value={equipo.id}>
                {equipo.nombre} - {equipo.colegio?.nombre || 'Sin colegio'}
              </option>
            ))}
          </select>
        </div>
      ) : (
        <div className="form-group">
          <label>Equipo asignado</label>
          <div className="assigned-team-info">
            <strong>{user?.equipo_nombre || 'Tu equipo'}</strong>
            <span className="team-note">(Se asignará automáticamente a tu equipo)</span>
          </div>
        </div>
      )}

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="nombre_apoderado">Nombre Apoderado</label>
          <input
            type="text"
            id="nombre_apoderado"
            name="nombre_apoderado"
            value={formData.nombre_apoderado}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="contacto_apoderado">Contacto Apoderado</label>
          <input
            type="text"
            id="contacto_apoderado"
            name="contacto_apoderado"
            value={formData.contacto_apoderado}
            onChange={handleInputChange}
            placeholder="Teléfono o email"
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="observaciones">Observaciones</label>
        <textarea
          id="observaciones"
          name="observaciones"
          value={formData.observaciones}
          onChange={handleInputChange}
          rows={3}
        />
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
        <button type="submit" disabled={loading} className="btn btn-primary">
          {loading ? 'Guardando...' : 'Agregar Estudiante'}
        </button>
      </div>
    </form>
  );
};

export default AddStudentForm;
