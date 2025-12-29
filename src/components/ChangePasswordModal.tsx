import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface ChangePasswordModalProps {
  onSuccess: () => void;
  isRequired?: boolean;
}

const ChangePasswordModal: React.FC<ChangePasswordModalProps> = ({ onSuccess, isRequired = false }) => {
  const { fetchWithAuth } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.new_password || !formData.confirm_password) {
      setError('Por favor completa todos los campos');
      return;
    }

    // Si no es requerido, necesitamos la contraseña actual
    if (!isRequired && !formData.current_password) {
      setError('Por favor completa todos los campos');
      return;
    }

    if (formData.new_password !== formData.confirm_password) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (formData.new_password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const payload: any = {
        new_password: formData.new_password
      };

      // Solo incluir current_password si no es requerido (ya cambió su contraseña antes)
      if (!isRequired) {
        if (formData.current_password) {
          payload.current_password = formData.current_password;
        } else {
          setError('Debes ingresar tu contraseña actual');
          setLoading(false);
          return;
        }
      }
      // Si es requerido, no enviamos current_password (el backend lo manejará)

      const response = await fetchWithAuth('/auth/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        onSuccess();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al cambiar la contraseña');
      }
    } catch (error) {
      console.error('Error al cambiar contraseña:', error);
      setError('Error de conexión al cambiar la contraseña');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>{isRequired ? 'Cambio de Contraseña Obligatorio' : 'Cambiar Contraseña'}</h3>
        </div>
        
        {isRequired && (
          <div className="warning-message">
            <p>Debes cambiar tu contraseña antes de continuar.</p>
          </div>
        )}
        
        <form className="tutor-form" onSubmit={handleSubmit}>
          {!isRequired && (
            <div className="form-group">
              <label htmlFor="current_password">Contraseña Actual *</label>
              <input
                type="password"
                id="current_password"
                name="current_password"
                value={formData.current_password}
                onChange={handleChange}
                required
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="new_password">Nueva Contraseña *</label>
            <input
              type="password"
              id="new_password"
              name="new_password"
              value={formData.new_password}
              onChange={handleChange}
              required
              minLength={6}
            />
            <small className="form-help-text">
              Mínimo 6 caracteres
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="confirm_password">Confirmar Nueva Contraseña *</label>
            <input
              type="password"
              id="confirm_password"
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              required
              minLength={6}
            />
          </div>

          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}

          <div className="form-actions">
            {!isRequired && (
              <button type="button" className="btn btn-secondary" onClick={onSuccess}>
                Cancelar
              </button>
            )}
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Cambiando...' : 'Cambiar Contraseña'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChangePasswordModal;

