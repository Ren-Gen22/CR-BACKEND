@echo off
setlocal enabledelayedexpansion

:: Function to simulate a progress bar
call :progress_bar 10 "Checking for Python 3.10..."

:: Check if Python 3.10 is installed
where py -3.10 >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python 3.10 is NOT installed.
    exit /b 1
) else (
    echo ✅ Python 3.10 is installed.
)

:: Check if venv module is available
call :progress_bar 10 "Checking if venv module is available..."
python -m venv --help >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ venv module is NOT available.
    echo Please install it using the appropriate command for your system.
    exit /b 1
) else (
    echo ✅ venv module is available.
)

:: Create virtual environment
python3.10 -m venv .myenv

:: Activate virtual environment
call :progress_bar 10 "Activating virtual environment..."
call .myenv\Scripts\activate
if %errorlevel% neq 0 (
    echo ❌ Failed to activate the virtual environment.
    exit /b 1
)

:: Upgrade pip
call :progress_bar 20 "Upgrading pip..."
pip install --upgrade pip >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Pip upgrade failed.
    exit /b 1
) else (
    echo ✅ Pip upgraded successfully.
)

:: Install dependencies if requirements.txt exists
if exist requirements.txt (
    call :progress_bar 10 "Installing dependencies..."
    pip install -r requirements.txt >nul 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies.
    ) else (
        echo ✅ Dependencies installed successfully.
    )
) else (
    echo ⚠️ No requirements.txt found. Skipping dependency installation.
)

echo 🎉 Setup completed successfully!
exit /b 0

:: Function to simulate a progress bar
:progress_bar
set /a progress=0
set duration=%1
set message=%2

set /a step=100/duration

echo %message%
<nul set /p="["
for /L %%i in (1,1,%duration%) do (
    ping -n 2 127.0.0.1 >nul
    set /a progress+=step
    <nul set /p="#"
)
echo ] %progress%%% complete.
exit /b
