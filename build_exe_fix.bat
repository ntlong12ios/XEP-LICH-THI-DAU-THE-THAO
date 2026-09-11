@echo off
set ROOT_DIR=d:\APP LONG VIET\XEP LICH THI DAU THE THAO
set TARGET_DIR=%ROOT_DIR%\App_Complete
set BACKEND_DIR=%ROOT_DIR%\backend

echo "Tat cac tien trinh dang chay de tranh loi xcopy..."
taskkill /F /IM XepLichThiDau.exe /T 2>NUL

echo "Copy frontend vào backend/frontend_dist..."
if exist "%BACKEND_DIR%\frontend_dist" rmdir /s /q "%BACKEND_DIR%\frontend_dist"
mkdir "%BACKEND_DIR%\frontend_dist"
xcopy "%ROOT_DIR%\frontend\dist\*" "%BACKEND_DIR%\frontend_dist\" /s /e /y

echo "Copy DATA.xlsx..."
copy "%ROOT_DIR%\DATA.xlsx" "%TARGET_DIR%\"

echo "Bắt đầu đóng gói PyInstaller..."
cd "%BACKEND_DIR%"
call venv\Scripts\activate.bat

:: Build with pyinstaller
:: Them co -y de ghi de thu muc dist cu
pyinstaller -y --name "XepLichThiDau" --windowed ^
  --add-data "frontend_dist;frontend_dist" ^
  --hidden-import "uvicorn.logging" ^
  --hidden-import "uvicorn.loops" ^
  --hidden-import "uvicorn.loops.auto" ^
  --hidden-import "uvicorn.protocols" ^
  --hidden-import "uvicorn.protocols.http" ^
  --hidden-import "uvicorn.protocols.http.auto" ^
  --hidden-import "uvicorn.protocols.websockets" ^
  --hidden-import "uvicorn.protocols.websockets.auto" ^
  --hidden-import "uvicorn.lifespan" ^
  --hidden-import "uvicorn.lifespan.on" ^
  --hidden-import "sqlalchemy.sql.default_comparator" ^
  --hidden-import "pandas" ^
  --hidden-import "openpyxl" ^
  --hidden-import "python-multipart" ^
  run_server.py

echo "Copy file exe ra thu muc hoan chinh..."
xcopy "dist\XepLichThiDau\*" "%TARGET_DIR%\" /s /e /y

echo "Hoan thanh!"
