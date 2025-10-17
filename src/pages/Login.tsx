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

  const handleDemoLogin = (demoEmail: string, demoPassword: string) => {
    setEmail(demoEmail);
    setPassword(demoPassword);
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
            <div className="demo-user">
              <strong>Administrador:</strong><br />
              Email: admin@tutorias.com<br />
              Contraseña: admin123
              <button 
                className="demo-button"
                onClick={() => handleDemoLogin('admin@tutorias.com', 'admin123')}
              >
                Usar estas credenciales
              </button>
            </div>
            <div className="demo-user">
              <strong>Tutor Equipo A:</strong><br />
              Email: tutor1@tutorias.com<br />
              Contraseña: tutor123
              <button 
                className="demo-button"
                onClick={() => handleDemoLogin('tutor1@tutorias.com', 'tutor123')}
              >
                Usar estas credenciales
              </button>
            </div>
            <div className="demo-user">
              <strong>Tutor Equipo B:</strong><br />
              Email: tutor2@tutorias.com<br />
              Contraseña: tutor123
              <button 
                className="demo-button"
                onClick={() => handleDemoLogin('tutor2@tutorias.com', 'tutor123')}
              >
                Usar estas credenciales
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;