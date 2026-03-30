#!/bin/bash
# Script de ejecución para el servidor Oracle
# Corre el pipeline completo: guion → audio → videos → render → subir a YouTube

cd "$(dirname "$0")"

export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

# Activar entorno virtual
source venv/bin/activate

# Ejecutar pipeline
python main.py >> logs/pipeline.log 2>&1
