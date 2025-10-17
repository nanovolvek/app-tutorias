#!/usr/bin/env python3
"""
Script simple para iniciar la aplicación sin inicializar la base de datos
"""

import uvicorn
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Iniciando aplicacion...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=False
    )
