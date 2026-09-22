@echo off
setlocal
cd /d "%~dp0"

where node >nul 2>nul
if errorlevel 1 (
  echo Node.js 20 or newer is required.
  pause
  exit /b 1
)

if not exist node_modules (
  echo Installing the locked project dependencies...
  call npm ci
  if errorlevel 1 goto :error
)

set "OPEN_BROWSER=1"
call npm run preview
exit /b %errorlevel%

:error
echo.
echo The local preview could not be started.
pause
exit /b 1
