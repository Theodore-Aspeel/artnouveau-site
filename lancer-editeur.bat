@echo off
setlocal

cd /d "%~dp0"
title Art Nouveau - editeur local

echo.
echo Editeur local des articles
echo ===========================
echo.
echo Une fenetre de navigateur va s'ouvrir automatiquement.
echo Si rien ne s'ouvre, allez a cette adresse :
echo.
echo   http://127.0.0.1:8765/
echo.
echo Gardez cette fenetre ouverte pendant l'utilisation.
echo Pour arreter l'editeur, fermez cette fenetre ou appuyez sur Ctrl+C.
echo.

where uv >nul 2>nul
if not errorlevel 1 goto use_uv

where py >nul 2>nul
if not errorlevel 1 goto use_py

goto use_python

:use_uv
uv run python -m tools.editorial_manager editor
goto after_editor

:use_py
py -m tools.editorial_manager editor
goto after_editor

:use_python
python -m tools.editorial_manager editor
goto after_editor

:after_editor

echo.
echo L'editeur s'est arrete.
echo Si le demarrage a echoue, verifiez que Python est installe.
pause
