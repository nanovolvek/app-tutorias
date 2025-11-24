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

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface StudentAttendanceData {
  student_id: number;
  student_name: string;
  course?: string;
  attendance_percentage: number;
  attended_weeks: number;
  absent_weeks: number;
  total_weeks: number;
}

interface AttendanceChartProps {
  data: StudentAttendanceData[];
  title?: string;
  xAxisLabel?: string;
}

const AttendanceChart: React.FC<AttendanceChartProps> = ({ data, title = 'Porcentaje de Asistencia', xAxisLabel = 'Personas' }) => {
  const chartData = {
    labels: data.map(student => student.student_name),
    datasets: [
      {
        label: '% de Asistencia',
        data: data.map(student => student.attendance_percentage),
        backgroundColor: data.map(student => {
          if (student.attendance_percentage >= 80) return 'rgba(34, 197, 94, 0.8)'; // Verde
          if (student.attendance_percentage >= 60) return 'rgba(251, 191, 36, 0.8)'; // Amarillo
          return 'rgba(239, 68, 68, 0.8)'; // Rojo
        }),
        borderColor: data.map(student => {
          if (student.attendance_percentage >= 80) return 'rgba(34, 197, 94, 1)';
          if (student.attendance_percentage >= 60) return 'rgba(251, 191, 36, 1)';
          return 'rgba(239, 68, 68, 1)';
        }),
        borderWidth: 1,
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
        text: title,
        font: {
          size: 16,
          weight: 'bold' as const,
        },
      },
      tooltip: {
        callbacks: {
          afterLabel: function(context: any) {
            const student = data[context.dataIndex];
            const tooltipLines = [];
            if (student.course) {
              tooltipLines.push(`Curso: ${student.course}`);
            }
            tooltipLines.push(
              `Semanas asistidas: ${student.attended_weeks}/${student.total_weeks}`,
              `Inasistencias: ${student.absent_weeks}`
            );
            return tooltipLines;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Porcentaje de Asistencia (%)'
        }
      },
      x: {
        title: {
          display: true,
          text: xAxisLabel
        }
      }
    },
  };

  return (
    <div className="attendance-chart-container">
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default AttendanceChart;