@echo off
setlocal

pushd "%~dp0"

set "PYTHON_CMD="

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=py -3"
    ) else (
        where python >nul 2>nul
        if not errorlevel 1 (
            set "PYTHON_CMD=python"
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo Could not find Python. Create the project virtual environment first, or install Python 3.
    echo.
    pause
    popd
    exit /b 1
)

echo Starting Liber Primus Operator Console...
%PYTHON_CMD% -m libreprimus.cli operator-console run
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo.
    echo Operator Console exited with code %EXIT_CODE%.
    echo If GUI dependencies are missing, install them with:
    echo   %PYTHON_CMD% -m pip install -e .[gui]
    echo.
    pause
)

popd
exit /b %EXIT_CODE%
