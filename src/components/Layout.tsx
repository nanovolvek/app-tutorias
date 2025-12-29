import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useEquipo } from '../hooks/useEquipo';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const { user, logout } = useAuth();
  const { equipoInfo } = useEquipo();

  const getMenuItems = () => {
    const baseItems = [
      { path: '/', label: 'Dashboard', icon: '📊' },
      { path: '/estudiantes', label: 'Estudiantes', icon: '👥' },
      { path: '/asistencia', label: 'Asistencia', icon: '✅' },
      { path: '/tickets', label: 'Tickets', icon: '🎫' },
      { path: '/prueba-diagnostico', label: 'Prueba Diagnóstico', icon: '📊' },
      { path: '/prueba-unidad', label: 'Prueba Unidad', icon: '📈' },
      { path: '/material-apoyo', label: 'Material de Apoyo', icon: '📚' },
    ];

    // Solo mostrar "Tutores" si es administrador
    if (user?.rol === 'admin') {
      baseItems.splice(2, 0, { path: '/tutores', label: 'Tutores', icon: '👨‍🏫' });
    }

    return baseItems;
  };

  const menuItems = getMenuItems();

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <h2>Plataforma Tutorías</h2>
          <button 
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ✕
          </button>
        </div>
        
        <div className="sidebar-content">
          {/* Información del equipo para tutores */}
          {user?.rol === 'tutor' && equipoInfo && (
            <div className="equipo-info">
              <div className="equipo-section">
                <h4>Tutores:</h4>
                <div className="tutores-list">
                  {equipoInfo.tutores.map((tutor, index) => (
                    <span key={tutor.id} className="tutor-name">
                      {tutor.nombre} {tutor.apellido}
                      {index < equipoInfo.tutores.length - 1 && ', '}
                    </span>
                  ))}
                </div>
              </div>
              {equipoInfo.colegio && (
                <div className="equipo-section">
                  <h4>Colegio:</h4>
                  <span className="colegio-name">{equipoInfo.colegio.nombre}</span>
                </div>
              )}
            </div>
          )}
          
          <nav className="sidebar-nav">
            <ul>
              {menuItems.map((item) => (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <span className="nav-icon">{item.icon}</span>
                    <span className="nav-label">{item.label}</span>
                  </Link>
                </li>
              ))}
            </ul>
            {/* Espacio adicional al final para facilitar scroll en móvil */}
            <div style={{ height: '200px', minHeight: '200px' }}></div>
          </nav>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="main-header">
          <button 
            className="mobile-menu-toggle"
            onClick={() => setSidebarOpen(true)}
          >
            ☰
          </button>
          <h1>Plataforma Tutorías</h1>
          <div className="user-info">
            <span>Hola, {user?.nombre_completo}</span>
            <span className="user-role">({user?.rol})</span>
            <button 
              className="logout-btn"
              onClick={logout}
              title="Cerrar sesión"
            >
              🚪
            </button>
          </div>
        </header>
        
        <div className="content">
          {children}
        </div>
      </main>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div 
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
};

export default Layout;
