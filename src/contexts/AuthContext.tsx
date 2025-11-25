import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchWithAuth } from '../utils/api';

interface User {
  id: number;
  email: string;
  nombre_completo: string;
  rol: string;
  equipo_id?: number;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  fetchWithAuth: (url: string, options?: RequestInit) => Promise<Response>;
  verifyToken: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    // Redirigir al login
    if (window.location.pathname !== '/') {
      window.location.href = '/';
    }
  };

  const verifyToken = async (): Promise<boolean> => {
    const currentToken = token || localStorage.getItem('token');
    if (!currentToken) {
      return false;
    }

    try {
      const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${currentToken}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setToken(currentToken);
        localStorage.setItem('token', currentToken);
        localStorage.setItem('user', JSON.stringify(userData));
        return true;
      } else {
        // Token inválido o expirado
        logout();
        return false;
      }
    } catch (error) {
      console.error('Error verificando token:', error);
      logout();
      return false;
    }
  };

  const handleFetchWithAuth = async (url: string, options: RequestInit = {}): Promise<Response> => {
    return fetchWithAuth(url, {
      ...options,
      token: token || localStorage.getItem('token'),
    });
  };

  useEffect(() => {
    // Verificar si hay un token guardado al cargar la aplicación
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
      
      // Verificar que el token sigue siendo válido
      verifyToken().catch(() => {
        // Si el token no es válido, limpiar y redirigir
        logout();
      });
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true);
    try {
        const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
        console.log('🔍 API URL:', apiUrl);
        console.log('🔍 Login URL:', `${apiUrl}/auth/login-json`);
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

      console.log('🔍 Response status:', response.status);
      console.log('🔍 Response ok:', response.ok);
      
      if (response.ok) {
        const data = await response.json();
        console.log('🔍 Login data:', data);
        setToken(data.access_token);
        
        // Obtener información del usuario
        console.log('🔍 Fetching user data from:', `${apiUrl}/auth/me`);
        const userResponse = await fetch(`${apiUrl}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${data.access_token}`,
          },
        });
        
        console.log('🔍 User response status:', userResponse.status);
        console.log('🔍 User response ok:', userResponse.ok);
        
        if (userResponse.ok) {
          const userData = await userResponse.json();
          console.log('🔍 User data:', userData);
          setUser(userData);
          localStorage.setItem('token', data.access_token);
          localStorage.setItem('user', JSON.stringify(userData));
          // Pequeño delay para asegurar que el estado se actualice
          setTimeout(() => {
            setIsLoading(false);
          }, 100);
          return true;
        } else {
          console.log('🔍 User fetch failed');
          setIsLoading(false);
          return false;
        }
      } else {
        console.log('🔍 Login failed with status:', response.status);
        const errorText = await response.text();
        console.log('🔍 Error response:', errorText);
        setIsLoading(false);
        return false;
      }
    } catch (error) {
      console.error('Error de login:', error);
      setIsLoading(false);
      return false;
    }
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    isLoading,
    login,
    logout,
    fetchWithAuth: handleFetchWithAuth,
    verifyToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};