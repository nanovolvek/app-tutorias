import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './AttendanceChart.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface StudentAttendanceSummary {
  student_id: number;
  student_name: string;
  course: string;
  school_name: string;
  total_weeks: number;
  attended_weeks: number;
  attendance_percentage: number;
  weekly_attendance: { [key: string]: boolean };
}

interface AttendanceChartProps {
  data: StudentAttendanceSummary[];
}

const AttendanceChart: React.FC<AttendanceChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="no-data">
        <p>No hay datos de asistencia disponibles</p>
      </div>
    );
  }

  // Preparar datos para el gráfico
  const chartData = {
    labels: data.map(student => student.student_name),
    datasets: [
      {
        label: '% de Asistencia',
        data: data.map(student => student.attendance_percentage),
        backgroundColor: data.map(student => {
          // Colores basados en el porcentaje de asistencia
          if (student.attendance_percentage >= 80) return 'rgba(34, 197, 94, 0.8)'; // Verde
          if (student.attendance_percentage >= 60) return 'rgba(251, 191, 36, 0.8)'; // Amarillo
          return 'rgba(239, 68, 68, 0.8)'; // Rojo
        }),
        borderColor: data.map(student => {
          if (student.attendance_percentage >= 80) return 'rgba(34, 197, 94, 1)';
          if (student.attendance_percentage >= 60) return 'rgba(251, 191, 36, 1)';
          return 'rgba(239, 68, 68, 1)';
        }),
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Porcentaje de Asistencia por Estudiante',
        font: {
          size: 16,
          weight: 'bold' as const,
        },
      },
      tooltip: {
        callbacks: {
          afterLabel: function(context: any) {
            const student = data[context.dataIndex];
            return [
              `Curso: ${student.course}`,
              `Colegio: ${student.school_name}`,
              `Semanas asistidas: ${student.attended_weeks}/${student.total_weeks}`,
            ];
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value: any) {
            return value + '%';
          },
        },
        title: {
          display: true,
          text: 'Porcentaje de Asistencia',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Estudiantes',
        },
      },
    },
  };

  return (
    <div className="attendance-chart-container">
      <div className="chart-wrapper">
        <Bar data={chartData} options={options} />
      </div>
      
      {/* Tabla de detalles */}
      <div className="attendance-table-container">
        <h3>Detalle de Asistencia por Semana</h3>
        <div className="table-wrapper">
          <table className="attendance-detail-table">
            <thead>
              <tr>
                <th>Estudiante</th>
                <th>Curso</th>
                <th>% Asistencia</th>
                {Array.from({ length: 10 }, (_, i) => (
                  <th key={i + 1}>S{i + 1}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((student) => (
                <tr key={student.student_id}>
                  <td className="student-name">{student.student_name}</td>
                  <td>{student.course}</td>
                  <td className={`attendance-percentage ${student.attendance_percentage >= 80 ? 'high' : student.attendance_percentage >= 60 ? 'medium' : 'low'}`}>
                    {student.attendance_percentage}%
                  </td>
                  {Array.from({ length: 10 }, (_, i) => {
                    const weekKey = `semana_${i + 1}`;
                    const attended = student.weekly_attendance[weekKey];
                    return (
                      <td key={i + 1} className={`week-cell ${attended ? 'attended' : 'absent'}`}>
                        {attended ? '✓' : '✗'}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AttendanceChart;
