# Script de Configuracion - IA Tutora
Write-Host "Configurando proyecto..." -ForegroundColor Cyan

# Eliminar venv antiguo
if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv
}

# Crear nuevo venv
python -m venv venv

# Activar y actualizar pip
. .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

Write-Host "Listo! Ejecuta: python test_connection.py" -ForegroundColor Green
