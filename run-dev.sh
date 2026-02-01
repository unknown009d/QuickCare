#!/bin/bash

echo "=== DEV START SCRIPT ==="

# ---------- BACKEND ----------
(
  echo "Starting Backend..."
  cd backend || exit 1

  if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
  fi

  source venv/bin/activate

  if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
  else
    echo "No requirements.txt found, skipping pip install"
  fi

  echo "Running backend server..."
  python app.py
) &

# ---------- FRONTEND ----------
(
  echo "Starting Frontend..."
  cd frontend || exit 1

  if ! command -v live-server &> /dev/null; then
    echo "live-server not found. Installing globally..."
    npm install -g live-server
  else
    echo "live-server already installed"
  fi

  echo "Running live-server..."
  live-server --port=5500
) &

wait

