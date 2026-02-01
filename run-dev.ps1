Write-Host "=== DEV START SCRIPT ===" -ForegroundColor Cyan

# ---------- BACKEND ----------
Start-Process powershell -ArgumentList "-NoExit", "-Command", {
    Write-Host "Starting Backend..." -ForegroundColor Yellow
    cd backend

    # Create venv if missing
    if (-Not (Test-Path "venv")) {
        Write-Host "Creating virtual environment..." -ForegroundColor Cyan
        py -3.13 -m venv venv
    }

    # Activate venv
    .\venv\Scripts\Activate.ps1

    # Install requirements if file exists
    if (Test-Path "requirements.txt") {
        Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
        pip install --upgrade pip
        pip install -r requirements.txt
    } else {
        Write-Host "No requirements.txt found, skipping pip install" -ForegroundColor DarkYellow
    }

    # Run backend
    Write-Host "Running backend server..." -ForegroundColor Green
    python app.py
}

# ---------- FRONTEND ----------
Start-Process powershell -ArgumentList "-NoExit", "-Command", {
    Write-Host "Starting Frontend..." -ForegroundColor Yellow
    cd frontend

    # Check live-server
    if (-Not (Get-Command live-server -ErrorAction SilentlyContinue)) {
        Write-Host "live-server not found. Installing globally..." -ForegroundColor Cyan
        npm install -g live-server
    } else {
        Write-Host "live-server already installed" -ForegroundColor Green
    }

    # Run live-server
    Write-Host "Running live-server..." -ForegroundColor Green
    live-server --port=5500
}

