import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Login.css';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, isLoading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const success = await login(email, password);
    
    if (!success) {
      setError('Email o contraseña incorrectos');
    }
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
        </form>

        <div className="login-demo">
          <h3>Credenciales de prueba:</h3>
          <div className="demo-credentials">
            <div>
              <strong>Administrador:</strong><br />
              Email: admin@tutorias.com<br />
              Contraseña: admin
            </div>
            <div>
              <strong>Tutor:</strong><br />
              Email: tutor@tutorias.com<br />
              Contraseña: tutor
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;