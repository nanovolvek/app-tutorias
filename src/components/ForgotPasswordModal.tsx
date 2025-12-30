import React, { useState } from 'react';

interface ForgotPasswordModalProps {
  onClose: () => void;
  onSuccess: () => void;
}

const ForgotPasswordModal: React.FC<ForgotPasswordModalProps> = ({ onClose, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [email, setEmail] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email) {
      setError('Por favor ingresa tu email');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/auth/request-password-reset`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess(true);
        // El token solo se muestra en desarrollo si SMTP no está configurado
        // En producción con SMTP configurado, el token se envía por email
        if (data.token && (import.meta as any).env?.DEV) {
          console.log('Token de recuperación (solo desarrollo, SMTP no configurado):', data.token);
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al solicitar recuperación');
      }
    } catch (error) {
      console.error('Error al solicitar recuperación:', error);
      setError('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="modal-overlay">
        <div className="modal-content">
          <div className="modal-header">
            <h3>Recuperación de Contraseña</h3>
            <button className="modal-close" onClick={onClose}>×</button>
          </div>
          
          <div className="modal-body">
            <div style={{ 
              background: '#ecfdf5', 
              border: '1px solid #10b981', 
              borderRadius: '8px', 
              padding: '16px',
              marginBottom: '20px'
            }}>
              <p style={{ color: '#059669', margin: 0 }}>
                Si el email existe en nuestro sistema, se enviará un enlace de recuperación.
                Por favor revisa tu correo electrónico.
              </p>
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-primary" onClick={onSuccess}>
                Entendido
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Recuperar Contraseña</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        <form className="tutor-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <small className="form-help-text">
              Ingresa tu email y te enviaremos un enlace para recuperar tu contraseña
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
              {loading ? 'Enviando...' : 'Enviar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ForgotPasswordModal;

