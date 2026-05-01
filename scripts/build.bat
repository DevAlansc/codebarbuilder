@echo off
setlocal

cd /d "%~dp0\.."

py -m PyInstaller packaging\codebarbuilder.spec --clean -y
if errorlevel 1 exit /b %errorlevel%

echo Build complete: dist\CodebarBuilder
