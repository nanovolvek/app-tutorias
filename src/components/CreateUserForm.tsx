import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Equipo {
  id: number;
  nombre: string;
  colegio?: {
    id: number;
    nombre: string;
  };
}

interface CreateUserFormProps {
  onSuccess: () => void;
  onClose: () => void;
  equipos: Equipo[];
}

const CreateUserForm: React.FC<CreateUserFormProps> = ({ onSuccess, onClose, equipos }) => {
  const { fetchWithAuth } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    email: '',
    nombre_completo: '',
    rol: 'tutor',
    equipo_id: '',
    password: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const generatePassword = () => {
    // Generar una contraseña aleatoria de 12 caracteres
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    let password = '';
    for (let i = 0; i < 12; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setFormData(prev => ({ ...prev, password }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.email || !formData.nombre_completo || !formData.password) {
      setError('Por favor completa todos los campos requeridos');
      return;
    }

    if (formData.rol === 'tutor' && !formData.equipo_id) {
      setError('Debes seleccionar un equipo para los tutores');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const payload: any = {
        email: formData.email,
        nombre_completo: formData.nombre_completo,
        rol: formData.rol,
        password: formData.password
      };

      if (formData.rol === 'tutor' && formData.equipo_id) {
        payload.equipo_id = parseInt(formData.equipo_id);
      }

      const response = await fetchWithAuth('/usuarios/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        onSuccess();
        onClose();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al crear el usuario');
      }
    } catch (error) {
      console.error('Error al crear usuario:', error);
      setError('Error de conexión al crear el usuario');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Crear Nuevo Usuario</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        <form className="tutor-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="nombre_completo">Nombre Completo *</label>
            <input
              type="text"
              id="nombre_completo"
              name="nombre_completo"
              value={formData.nombre_completo}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="rol">Rol *</label>
            <select
              id="rol"
              name="rol"
              value={formData.rol}
              onChange={handleChange}
              required
            >
              <option value="tutor">Tutor</option>
              <option value="admin">Administrador</option>
            </select>
          </div>

          {formData.rol === 'tutor' && (
            <div className="form-group">
              <label htmlFor="equipo_id">Equipo *</label>
              <select
                id="equipo_id"
                name="equipo_id"
                value={formData.equipo_id}
                onChange={handleChange}
                required
              >
                <option value="">Seleccionar equipo</option>
                {equipos.map(equipo => (
                  <option key={equipo.id} value={equipo.id}>
                    {equipo.nombre} - {equipo.colegio?.nombre || 'Sin colegio'}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">Contraseña Temporal *</label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="text"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                style={{ flex: 1 }}
              />
              <button
                type="button"
                className="btn btn-info"
                onClick={generatePassword}
                style={{ whiteSpace: 'nowrap' }}
              >
                Generar
              </button>
            </div>
            <small className="form-help-text">
              El usuario deberá cambiar esta contraseña al iniciar sesión por primera vez
            </small>
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
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Creando...' : 'Crear Usuario'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateUserForm;

