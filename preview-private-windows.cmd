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

if not exist .private-media\blue-01-overview-19126.jpg (
  echo.
  echo Private photographs are missing.
  echo Copy the 12 extracted review JPEG files into .private-media\
  echo using the filenames documented in research/d1-image-first-private-preview.md.
  echo Nothing from this folder is added to Git or the public build.
  pause
  exit /b 1
)

set "PRIVATE_PREVIEW=1"
set "PRIVATE_PREVIEW_MEDIA_DIR=%CD%\.private-media"
set "OPEN_BROWSER=1"
call npm run preview:private
exit /b %errorlevel%

:error
echo.
echo The private local preview could not be started.
pause
exit /b 1
