@echo off
echo ===================================================
echo Starting SmartTriage AI System
echo ===================================================
echo.

echo [1/2] Starting FastAPI Backend on port 8000...
start "SmartTriage Backend" cmd /k "python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"

echo [2/2] Starting Nuxt Frontend on port 3000...
start "SmartTriage Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both services have been launched in separate windows!
echo - Backend API: http://127.0.0.1:8000
echo - Frontend UI: http://localhost:3000
echo.
echo Close this window or the newly opened windows to stop the servers.
