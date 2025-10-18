# Usar Python 3.9 como imagen base
FROM python:3.9-slim

# Instalar Node.js para construir el frontend
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY backend/requirements.txt .
COPY frontend/package*.json ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias de Node.js
RUN npm ci

# Copiar código fuente
COPY . .

# Construir el frontend
RUN cd frontend && npm run build

# Crear directorio para archivos estáticos
RUN mkdir -p /app/static

# Copiar archivos construidos del frontend
RUN cp -r frontend/dist/* /app/static/

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Exponer puerto (Render usa el puerto de la variable PORT)
EXPOSE $PORT

# Comando para inicializar la base de datos y ejecutar la aplicación
CMD ["sh", "-c", "python init_database.py && cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
