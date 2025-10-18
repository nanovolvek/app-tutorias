@echo off
echo 🐳 Construyendo y ejecutando la aplicación con Docker...
echo.

echo 📦 Construyendo la imagen Docker...
docker-compose build

echo.
echo 🚀 Iniciando los servicios...
docker-compose up

echo.
echo ✅ Aplicación ejecutándose en http://localhost:8000
echo 📊 Base de datos PostgreSQL en localhost:5432
echo.
echo Para detener: Ctrl+C
pause
