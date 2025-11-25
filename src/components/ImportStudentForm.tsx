import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Equipo {
  id: number;
  nombre: string;
  colegio_id?: number;
  colegio_nombre?: string;
  colegio_comuna?: string;
}

interface ImportStudentFormProps {
  onSuccess: () => void;
  onClose: () => void;
}

const ImportStudentForm: React.FC<ImportStudentFormProps> = ({ onSuccess, onClose }) => {
  const { fetchWithAuth } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    fetchEquipos();
  }, []);

  const fetchEquipos = async () => {
    try {
      const response = await fetchWithAuth('/equipos/con-colegios/');
      if (response.ok) {
        const data = await response.json();
        setEquipos(data);
      }
    } catch (error) {
      console.error('Error al cargar equipos:', error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (!selectedFile.name.endsWith('.xlsx') && !selectedFile.name.endsWith('.xls')) {
        setError('El archivo debe ser un Excel (.xlsx o .xls)');
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError('');
      setResult(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Por favor selecciona un archivo Excel');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetchWithAuth('/estudiantes/import', {
        method: 'POST',
        body: formData,
        headers: {} // No establecer Content-Type, el navegador lo hará automáticamente con el boundary
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
        if (data.created > 0) {
          setTimeout(() => {
            onSuccess();
            onClose();
          }, 2000);
        }
      } else {
        setError(data.detail || 'Error al importar el archivo');
      }
    } catch (error: any) {
      console.error('Error al importar:', error);
      setError(error.message || 'Error de conexión al importar el archivo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto' }}>
        <div className="modal-header">
          <h2>Importar Estudiantes desde Excel</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {/* Instrucciones */}
          <div style={{ marginBottom: '24px', padding: '16px', backgroundColor: '#f0f9ff', borderRadius: '8px', border: '1px solid #bae6fd' }}>
            <h3 style={{ marginTop: 0, color: '#0369a1' }}>📋 Instrucciones para el archivo Excel</h3>
            <ol style={{ marginBottom: '16px', paddingLeft: '20px' }}>
              <li>El archivo debe ser un Excel (.xlsx o .xls)</li>
              <li>La primera fila debe contener los siguientes encabezados (exactamente como se muestra):</li>
            </ol>
            <div style={{ backgroundColor: 'white', padding: '12px', borderRadius: '4px', marginBottom: '16px', fontFamily: 'monospace', fontSize: '0.9rem', overflowX: 'auto' }}>
              <strong>RUT | Nombre | Apellido | Curso | Equipo ID | Nombre Apoderado | Contacto Apoderado | Observaciones</strong>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <strong>Campos requeridos:</strong>
              <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                <li><strong>RUT:</strong> Formato XX.XXX.XXX-X o X.XXX.XXX-X (ejemplo: 12.345.678-9)</li>
                <li><strong>Nombre:</strong> Nombre del estudiante</li>
                <li><strong>Apellido:</strong> Apellido del estudiante</li>
                <li><strong>Curso:</strong> Curso del estudiante</li>
                <li><strong>Equipo ID:</strong> ID numérico del equipo (ver tabla abajo)</li>
              </ul>
            </div>
            <div>
              <strong>Campos opcionales:</strong>
              <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                <li><strong>Nombre Apoderado:</strong> Nombre del apoderado</li>
                <li><strong>Contacto Apoderado:</strong> Teléfono o email del apoderado</li>
                <li><strong>Observaciones:</strong> Notas adicionales</li>
              </ul>
            </div>
          </div>

          {/* Tabla de Equipos */}
          <div style={{ marginBottom: '24px' }}>
            <h3 style={{ marginBottom: '12px' }}>📊 Equipos Disponibles</h3>
            <div style={{ maxHeight: '200px', overflowY: 'auto', border: '1px solid #e5e7eb', borderRadius: '4px' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                <thead style={{ backgroundColor: '#f3f4f6', position: 'sticky', top: 0 }}>
                  <tr>
                    <th style={{ padding: '8px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>ID</th>
                    <th style={{ padding: '8px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Equipo</th>
                    <th style={{ padding: '8px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Colegio</th>
                    <th style={{ padding: '8px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Comuna</th>
                  </tr>
                </thead>
                <tbody>
                  {equipos.map((equipo) => (
                    <tr key={equipo.id}>
                      <td style={{ padding: '8px', borderBottom: '1px solid #e5e7eb' }}><strong>{equipo.id}</strong></td>
                      <td style={{ padding: '8px', borderBottom: '1px solid #e5e7eb' }}>{equipo.nombre}</td>
                      <td style={{ padding: '8px', borderBottom: '1px solid #e5e7eb' }}>{equipo.colegio_nombre || 'Sin colegio'}</td>
                      <td style={{ padding: '8px', borderBottom: '1px solid #e5e7eb' }}>{equipo.colegio_comuna || 'Sin comuna'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Formulario de carga */}
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '16px' }}>
              <label htmlFor="file-input" style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Seleccionar archivo Excel:
              </label>
              <input
                id="file-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileChange}
                disabled={loading}
                style={{ width: '100%', padding: '8px', border: '1px solid #d1d5db', borderRadius: '4px' }}
              />
              {file && (
                <p style={{ marginTop: '8px', color: '#059669', fontSize: '0.9rem' }}>
                  ✓ Archivo seleccionado: {file.name}
                </p>
              )}
            </div>

            {error && (
              <div style={{ padding: '12px', backgroundColor: '#fee2e2', color: '#991b1b', borderRadius: '4px', marginBottom: '16px' }}>
                {error}
              </div>
            )}

            {result && (
              <div style={{ marginBottom: '16px' }}>
                <div style={{ padding: '12px', backgroundColor: result.created > 0 ? '#dcfce7' : '#fef3c7', borderRadius: '4px', marginBottom: '12px' }}>
                  <p style={{ margin: 0, fontWeight: '600', color: result.created > 0 ? '#166534' : '#92400e' }}>
                    {result.message}
                  </p>
                  {result.total_errors > 0 && (
                    <p style={{ margin: '8px 0 0 0', fontSize: '0.9rem', color: result.created > 0 ? '#166534' : '#92400e' }}>
                      Se encontraron {result.total_errors} error(es)
                    </p>
                  )}
                </div>
                {result.errors && result.errors.length > 0 && (
                  <div style={{ maxHeight: '200px', overflowY: 'auto', padding: '12px', backgroundColor: '#fef2f2', borderRadius: '4px', border: '1px solid #fecaca' }}>
                    <strong style={{ color: '#991b1b', display: 'block', marginBottom: '8px' }}>Errores encontrados:</strong>
                    <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '0.85rem', color: '#991b1b' }}>
                      {result.errors.map((err: string, idx: number) => (
                        <li key={idx} style={{ marginBottom: '4px' }}>{err}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
              <button
                type="button"
                onClick={onClose}
                disabled={loading}
                className="btn btn-secondary"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={loading || !file}
                className="btn btn-primary"
              >
                {loading ? 'Importando...' : 'Importar'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ImportStudentForm;

