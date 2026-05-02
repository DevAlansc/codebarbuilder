@echo off
setlocal

cd /d "%~dp0\.."

call scripts\build.bat
if errorlevel 1 exit /b %errorlevel%

set "ISCC=ISCC.exe"
where ISCC.exe >nul 2>nul
if errorlevel 1 (
    if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
        set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
    ) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
        set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
    ) else (
        echo Inno Setup 6 is required to build the Windows installer.
        echo Install it and make sure ISCC.exe is available in PATH.
        exit /b 1
    )
)

"%ISCC%" packaging\windows\codebarbuilder.iss
if errorlevel 1 exit /b %errorlevel%

echo Installer complete: dist\installer\CodebarBuilder-Setup-0.1.0.exe
