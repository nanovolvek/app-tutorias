import React from 'react';

const MaterialApoyo: React.FC = () => {
  const handleAccessDrive = () => {
    // Abrir el Google Drive en una nueva pestaña
    window.open('https://drive.google.com/drive/u/1/folders/1G4DkmD7e2jBUBywkLhWiTYK0PFsW-_vW', '_blank');
  };

  return (
    <div className="page-container">
      <div className="material-apoyo-container">
        <div className="material-header">
          <h1 className="page-title">📚 Material de Apoyo</h1>
          <p className="page-description">
            Accede a todos los recursos educativos, guías y documentos compartidos para el programa de tutorías.
          </p>
        </div>

        <div className="drive-access-card">
          <div className="drive-icon">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M7.71 6.705L12 2.415L16.29 6.705H7.71Z" fill="#4285F4"/>
              <path d="M7.71 6.705H16.29L12 11L7.71 6.705Z" fill="#34A853"/>
              <path d="M7.71 6.705L12 11L16.29 6.705L12 2.415L7.71 6.705Z" fill="#FBBC04"/>
              <path d="M7.71 6.705L12 11L7.71 15.295L7.71 6.705Z" fill="#EA4335"/>
              <path d="M16.29 6.705L12 11L16.29 15.295L16.29 6.705Z" fill="#34A853"/>
            </svg>
          </div>
          
          <h2 className="drive-title">Google Drive</h2>
          <p className="drive-description">
            Haz clic en el botón para acceder al repositorio de material de apoyo en Google Drive.
            <br />
            <strong>Nota:</strong> Deberás iniciar sesión con tu cuenta de Google autorizada.
          </p>
          
          <button 
            className="drive-access-button"
            onClick={handleAccessDrive}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
            </svg>
            Acceder al Material
          </button>
        </div>

        <div className="access-info">
          <div className="info-item">
            <div className="info-icon">🔐</div>
            <div className="info-text">
              <h3>Acceso Seguro</h3>
              <p>El material está protegido y solo accesible para usuarios autorizados del programa.</p>
            </div>
          </div>
          
          <div className="info-item">
            <div className="info-icon">📁</div>
            <div className="info-text">
              <h3>Organización</h3>
              <p>Encuentra recursos organizados por materias, niveles y tipos de contenido.</p>
            </div>
          </div>
          
          <div className="info-item">
            <div className="info-icon">🔄</div>
            <div className="info-text">
              <h3>Actualizaciones</h3>
              <p>El contenido se actualiza regularmente con nuevos materiales y recursos.</p>
            </div>
          </div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{
        __html: `
          .material-apoyo-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
          }

          .material-header {
            text-align: center;
            margin-bottom: 3rem;
          }

          .page-title {
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 1rem;
            font-weight: 700;
          }

          .page-description {
            font-size: 1.1rem;
            color: #718096;
            line-height: 1.6;
            max-width: 600px;
            margin: 0 auto;
          }

          .drive-access-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
            color: white;
            margin-bottom: 3rem;
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
          }

          .drive-access-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
          }

          .drive-icon {
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: center;
          }

          .drive-title {
            font-size: 2rem;
            margin-bottom: 1rem;
            font-weight: 600;
          }

          .drive-description {
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            opacity: 0.9;
          }

          .drive-access-button {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            backdrop-filter: blur(10px);
          }

          .drive-access-button:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
          }

          .access-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
          }

          .info-item {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            padding: 1.5rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
          }

          .info-item:hover {
            transform: translateY(-3px);
          }

          .info-icon {
            font-size: 2rem;
            flex-shrink: 0;
          }

          .info-text h3 {
            font-size: 1.2rem;
            color: #2d3748;
            margin-bottom: 0.5rem;
            font-weight: 600;
          }

          .info-text p {
            color: #718096;
            line-height: 1.5;
            margin: 0;
          }

          @media (max-width: 768px) {
            .material-apoyo-container {
              padding: 1rem;
            }

            .page-title {
              font-size: 2rem;
            }

            .drive-access-card {
              padding: 2rem;
            }

            .drive-title {
              font-size: 1.5rem;
            }

            .access-info {
              grid-template-columns: 1fr;
              gap: 1rem;
            }
          }
        `
      }} />
    </div>
  );
};

export default MaterialApoyo;
