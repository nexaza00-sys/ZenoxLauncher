@echo off
setlocal EnableExtensions

REM ============================================================
REM  ZENOX GD LAUNCHER  -  Build Script v2.0
REM  Created by SONI
REM  Compiles the .exe and prepares everything for Inno Setup
REM ============================================================

title ZenoxGD Launcher - Build

echo.
echo   ********************************************
echo   *   ZENOX GD LAUNCHER - Build Script       *
echo   *   Created by SONI                         *
echo   ********************************************
echo.

REM ── Step 0: Check Python ────────────────────────────────
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo   [ERROR] Python no esta instalado o no esta en PATH.
    echo           Descargalo de: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo   Python encontrado:
python --version

REM ── Step 1: Create virtual environment (optional) ──────
if not exist "venv" (
    echo.
    echo   [1/5] Creando entorno virtual...
    python -m venv venv
) else (
    echo.
    echo   [1/5] Entorno virtual ya existe.
)

REM ── Step 2: Activate venv and install deps ──────────────
echo.
echo   [2/5] Instalando dependencias...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM ── Step 3: Create assets directory if missing ──────────
if not exist "assets" mkdir assets

echo.
echo   [3/5] Compilando ejecutable con PyInstaller...

echo.
REM ── Build onefile (self-contained .exe) ─────────────────
pyinstaller --noconfirm --onefile --windowed ^
  --name "ZenoxGD Launcher" ^
  --add-data "assets;assets" ^
  main.py

echo.

REM ── Step 4: Verify build ────────────────────────────────
echo   [4/5] Verificando build...
if exist "dist\ZenoxGD Launcher.exe" (
    echo.
    echo   ============================================
    echo    [OK] Ejecutable creado exitosamente!
    echo    Archivo: dist\ZenoxGD Launcher.exe
    echo   ============================================
    
    REM Show file size
    for %%A in ("dist\ZenoxGD Launcher.exe") do (
        echo    Tamano: %%~zA bytes
    )
) else (
    echo.
    echo   [ERROR] No se pudo crear el ejecutable.
    echo           Revisa los errores de PyInstaller arriba.
    pause
    exit /b 1
)

REM ── Step 5: Prepare Inno Setup ──────────────────────────
echo.
echo   [5/5] Preparando para Inno Setup...
echo.
echo   ==============================================
echo    INSTRUCCIONES PARA CREAR EL INSTALADOR:
echo   ==============================================
echo.
echo    1. Descarga Inno Setup desde:
echo       https://jrsoftware.org/isdl.php
echo.
echo    2. Abre ZenoxGD_Installer.iss en Inno Setup
echo.
echo    3. Compila el instalador (Ctrl+F9)
echo.
echo    4. El instalador se generara en:
echo       Output\ZenoxGD_Launcher_Setup_v1.0.0.exe
echo.
echo   ==============================================

call deactivate
pause
