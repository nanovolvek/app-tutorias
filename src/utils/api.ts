/**
 * Helper para hacer peticiones fetch con autenticación y manejo automático de errores 401
 */

interface FetchOptions extends RequestInit {
  token?: string | null;
  skipAuth?: boolean;
}

export async function fetchWithAuth(
  url: string,
  options: FetchOptions = {}
): Promise<Response> {
  const { token, skipAuth, ...fetchOptions } = options;
  const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';
  const fullUrl = url.startsWith('http') ? url : `${apiUrl}${url}`;

  // Headers por defecto
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(fetchOptions.headers as Record<string, string>),
  };

  // Agregar token de autenticación si está disponible y no se omite
  if (!skipAuth && token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(fullUrl, {
      ...fetchOptions,
      headers,
    });

    // Si recibimos un 401 (Unauthorized), el token expiró o es inválido
    if (response.status === 401 && !skipAuth) {
      // Limpiar datos de autenticación
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // Redirigir al login si no estamos ya ahí
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/';
      }
      
      // Lanzar error para que el componente pueda manejarlo
      throw new Error('Token expirado o inválido. Por favor, inicia sesión nuevamente.');
    }

    return response;
  } catch (error) {
    // Si es un error de red, re-lanzarlo
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Error de conexión. Por favor, verifica tu conexión a internet.');
    }
    throw error;
  }
}

