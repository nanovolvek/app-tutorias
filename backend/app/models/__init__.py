from app.database import Base
from .user import Usuario
from .school import Colegio
from .tutor import Tutor
from .student import Estudiante
from .equipo import Equipo
from .attendance import AsistenciaEstudiante, AsistenciaTutor, EstadoAsistencia
from .tickets import TicketEstudiante, EstadoTicket
from .prueba_diagnostico import PruebaDiagnosticoEstudiante, PorcentajeLogro as PorcentajeLogroDiagnostico
from .prueba_unidad import PruebaUnidadEstudiante, PorcentajeLogro as PorcentajeLogroUnidad
