import React from 'react';

const Estudiantes: React.FC = () => {
  return (
    <div className="page-container">
      <h1 className="page-title">Estudiantes</h1>
      <p className="page-description">
        Gestiona la información de todos los estudiantes del programa de tutorías. 
        Aquí podrás consultar datos personales, historial académico y estado actual.
      </p>
    </div>
  );
};

export default Estudiantes;
