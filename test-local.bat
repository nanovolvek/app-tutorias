@echo off
echo 🐳 Probando la aplicación localmente con Docker...
echo.

echo 📦 Construyendo la imagen Docker...
docker build -t tutorias-app .

echo.
echo 🚀 Ejecutando la aplicación...
echo.
echo ✅ Aplicación disponible en: http://localhost:8000
echo 📊 Base de datos: PostgreSQL en localhost:5432
echo.
echo Para detener: Ctrl+C
echo.

docker run -p 8000:8000 -e DATABASE_URL=postgresql://postgres:tutorias123@host.docker.internal:5432/tutorias_db -e SECRET_KEY=tutorias-local-secret -e ALLOWED_ORIGINS=http://localhost:8000,http://localhost:5173 tutorias-app

pause
