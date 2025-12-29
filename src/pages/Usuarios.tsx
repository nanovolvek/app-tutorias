import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import CreateUserForm from '../components/CreateUserForm';
import { useIsMobile } from '../hooks/useIsMobile';

interface Equipo {
  id: number;
  nombre: string;
  colegio?: {
    id: number;
    nombre: string;
  };
}

interface Usuario {
  id: number;
  email: string;
  nombre_completo: string;
  rol: string;
  equipo_id?: number;
  is_active: boolean;
  password_changed: boolean;
  created_at: string;
  equipo?: Equipo;
}

const Usuarios: React.FC = () => {
  const { fetchWithAuth, user } = useAuth();
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const isMobile = useIsMobile();

  const fetchUsuarios = async () => {
    try {
      const response = await fetchWithAuth('/usuarios/');
      if (response.ok) {
        const data = await response.json();
        setUsuarios(data);
      } else {
        setError('Error al cargar los usuarios');
      }
    } catch (error) {
      console.error('Error al cargar usuarios:', error);
      setError('Error de conexión al cargar los usuarios');
    } finally {
      setLoading(false);
    }
  };

  const fetchEquipos = async () => {
    try {
      const response = await fetchWithAuth('/equipos/');
      if (response.ok) {
        const data = await response.json();
        setEquipos(data);
      }
    } catch (error) {
      console.error('Error al cargar equipos:', error);
    }
  };

  useEffect(() => {
    if (user?.rol === 'admin') {
      fetchUsuarios();
      fetchEquipos();
    }
  }, [user]);

  if (user?.rol !== 'admin') {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <h2>Acceso Denegado</h2>
        <p>No tienes permisos para acceder a esta página.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <div style={{ 
          width: '40px', 
          height: '40px', 
          border: '4px solid #e2e8f0',
          borderTop: '4px solid #667eea',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
          margin: '0 auto'
        }}></div>
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
        <p style={{ marginTop: '1rem' }}>Cargando usuarios...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '2rem' }}>
      <div className="section-header">
        <h1>Gestión de Usuarios</h1>
        <div className="action-buttons">
          <button 
            className="btn btn-primary"
            onClick={() => setShowCreateForm(true)}
          >
            + Crear Usuario
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message" style={{ marginBottom: '1rem' }}>
          <p>{error}</p>
        </div>
      )}

      {showCreateForm && (
        <CreateUserForm
          onSuccess={() => {
            fetchUsuarios();
            setShowCreateForm(false);
          }}
          onClose={() => setShowCreateForm(false)}
          equipos={equipos}
        />
      )}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Nombre Completo</th>
              <th>Rol</th>
              <th>Equipo</th>
              <th>Estado</th>
              <th>Contraseña Cambiada</th>
              <th>Fecha Creación</th>
            </tr>
          </thead>
          <tbody>
            {usuarios.length === 0 ? (
              <tr>
                <td colSpan={8} style={{ textAlign: 'center', padding: '2rem' }}>
                  No hay usuarios registrados
                </td>
              </tr>
            ) : (
              usuarios.map((usuario) => (
                <tr key={usuario.id}>
                  <td>{usuario.id}</td>
                  <td>{usuario.email}</td>
                  <td>{usuario.nombre_completo}</td>
                  <td>
                    <span style={{
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.85rem',
                      fontWeight: 600,
                      background: usuario.rol === 'admin' ? '#dbeafe' : '#f0fdf4',
                      color: usuario.rol === 'admin' ? '#1e40af' : '#166534'
                    }}>
                      {usuario.rol === 'admin' ? 'Admin' : 'Tutor'}
                    </span>
                  </td>
                  <td>{usuario.equipo?.nombre || '-'}</td>
                  <td>
                    <span style={{
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.85rem',
                      fontWeight: 600,
                      background: usuario.is_active ? '#ecfdf5' : '#fef2f2',
                      color: usuario.is_active ? '#059669' : '#dc2626'
                    }}>
                      {usuario.is_active ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td>
                    <span style={{
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.85rem',
                      fontWeight: 600,
                      background: usuario.password_changed ? '#ecfdf5' : '#fef3c7',
                      color: usuario.password_changed ? '#059669' : '#d97706'
                    }}>
                      {usuario.password_changed ? 'Sí' : 'No'}
                    </span>
                  </td>
                  <td>{new Date(usuario.created_at).toLocaleDateString('es-CL')}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Usuarios;

