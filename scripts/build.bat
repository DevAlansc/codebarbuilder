@echo off
setlocal

cd /d "%~dp0\.."

py scripts\generate_windows_icon.py
if errorlevel 1 exit /b %errorlevel%

py -m PyInstaller packaging\codebarbuilder.spec --clean -y
if errorlevel 1 exit /b %errorlevel%

echo Build complete: dist\CodebarBuilder
