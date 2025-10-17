import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Tutor {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
}

interface Colegio {
  id: number;
  nombre: string;
  comuna: string;
}

interface EquipoInfo {
  id: number;
  nombre: string;
  descripcion: string | null;
  colegio_id: number | null;
  tutores: Tutor[];
  colegio: Colegio | null;
}

export const useEquipo = () => {
  const [equipoInfo, setEquipoInfo] = useState<EquipoInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user, token } = useAuth();

  useEffect(() => {
    const fetchEquipoInfo = async () => {
      // Solo hacer fetch si es un tutor y tiene equipo_id
      if (user?.rol !== 'tutor' || !user?.equipo_id || !token) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/equipos/mi-equipo/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          setEquipoInfo(data);
        } else {
          setError('Error al obtener información del equipo');
        }
      } catch (err) {
        setError('Error de conexión');
        console.error('Error fetching equipo info:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchEquipoInfo();
  }, [user, token]);

  return { equipoInfo, loading, error };
};
