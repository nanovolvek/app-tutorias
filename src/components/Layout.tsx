import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const { user, logout } = useAuth();

  const getMenuItems = () => {
    const baseItems = [
      { path: '/', label: 'Dashboard', icon: '📊' },
      { path: '/estudiantes', label: 'Estudiantes', icon: '👥' },
      { path: '/asistencia', label: 'Asistencia', icon: '✅' },
      { path: '/pruebas', label: 'Pruebas', icon: '📝' },
      { path: '/tickets', label: 'Tickets', icon: '🎫' },
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
        </nav>
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
