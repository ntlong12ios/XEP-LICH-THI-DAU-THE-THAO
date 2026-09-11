@echo off
chcp 65001 >nul
echo ========================================================
echo   KHOI DONG PHAN MEM XEP LICH THI DAU THE THAO
echo ========================================================
echo.

echo [1/2] Dang khoi dong Backend (FastAPI) o cong 8000...
start "Backend - FastAPI" cmd /k "cd /d "%~dp0backend" && .\venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Dang khoi dong Frontend (React Vite) o cong 5173...
start "Frontend - React" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================================
echo Hoan tat! Vui long doi 3-5 giay de he thong san sang.
echo Trinh duyet se duoc mo tai: http://localhost:5173
echo ========================================================
echo (Giu nguyen 2 cua so den hien len de phan mem hoat dong)
echo.
pause
