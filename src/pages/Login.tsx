import React, { useState, useEffect } from 'react';
import ChangePasswordModal from '../components/ChangePasswordModal';
import ForgotPasswordModal from '../components/ForgotPasswordModal';
import './Login.css';

const Login: React.FC = () => {
  useEffect(() => {
    // Agregar clase al body y root para permitir scroll
    document.body.classList.add('login-page');
    const root = document.getElementById('root');
    if (root) {
      root.classList.add('login-page');
    }
    
    return () => {
      // Limpiar al desmontar
      document.body.classList.remove('login-page');
      if (root) {
        root.classList.remove('login-page');
      }
    };
  }, []);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/auth/login-json`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.access_token;
        
        // Guardar token temporalmente
        localStorage.setItem('token', token);
        
        // Obtener información del usuario
        const userResponse = await fetch(`${apiUrl}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        
        if (userResponse.ok) {
          const userData = await userResponse.json();
          localStorage.setItem('user', JSON.stringify(userData));
          
          // Verificar si necesita cambiar contraseña
          if (data.requires_password_change || !userData.password_changed) {
            setShowChangePassword(true);
          } else {
            // Login exitoso, recargar para actualizar el contexto
            window.location.reload();
          }
        } else {
          setError('Error al obtener información del usuario');
        }
      } else {
        setError('Email o contraseña incorrectos');
      }
    } catch (error) {
      console.error('Error de login:', error);
      setError('Error de conexión');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePasswordChanged = () => {
    setShowChangePassword(false);
    // Recargar para actualizar el contexto
    window.location.reload();
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>Plataforma Tutorías</h1>
          <p>Inicia sesión para acceder al sistema</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@email.com"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Tu contraseña"
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={isLoading} className="login-button">
            {isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </button>

          <div style={{ textAlign: 'center', marginTop: '1rem' }}>
            <button
              type="button"
              onClick={() => setShowForgotPassword(true)}
              style={{
                background: 'none',
                border: 'none',
                color: '#667eea',
                cursor: 'pointer',
                textDecoration: 'underline',
                fontSize: '0.875rem'
              }}
            >
              ¿Olvidaste tu contraseña?
            </button>
          </div>
        </form>
      </div>

      {showChangePassword && (
        <ChangePasswordModal
          isRequired={true}
          onSuccess={handlePasswordChanged}
        />
      )}

      {showForgotPassword && (
        <ForgotPasswordModal
          onClose={() => setShowForgotPassword(false)}
          onSuccess={() => setShowForgotPassword(false)}
        />
      )}
    </div>
  );
};

export default Login;