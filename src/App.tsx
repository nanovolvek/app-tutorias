import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import Estudiantes from './pages/Estudiantes';
import Tutores from './pages/Tutores';
import Usuarios from './pages/Usuarios';
import Asistencia from './pages/Asistencia';
import Tickets from './pages/Tickets';
import PruebaDiagnostico from './pages/PruebaDiagnostico';
import PruebaUnidad from './pages/PruebaUnidad';
import MaterialApoyo from './pages/MaterialApoyo';

function AppContent() {
  const { isAuthenticated, isLoading, user, token } = useAuth();

  if (isLoading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontSize: '1.2rem',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            width: '40px', 
            height: '40px', 
            border: '4px solid rgba(255,255,255,0.3)',
            borderTop: '4px solid white',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem'
          }}></div>
          Cargando...
        </div>
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  if (!isAuthenticated || !user || !token) {
    return (
      <Routes>
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="*" element={<Login />} />
      </Routes>
    );
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/estudiantes" element={<Estudiantes />} />
        <Route path="/tutores" element={<Tutores />} />
        <Route path="/usuarios" element={<Usuarios />} />
        <Route path="/asistencia" element={<Asistencia />} />
        <Route path="/tickets" element={<Tickets />} />
        <Route path="/prueba-diagnostico" element={<PruebaDiagnostico />} />
        <Route path="/prueba-unidad" element={<PruebaUnidad />} />
        <Route path="/material-apoyo" element={<MaterialApoyo />} />
      </Routes>
    </Layout>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
