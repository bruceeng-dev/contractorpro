@echo off
:loop
cls
echo ================================================
echo Pokemon OCR Progress Monitor
echo ================================================
echo Time: %TIME%
echo.

REM Check if Python is running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Status: RUNNING
    echo.

    REM Show Python process details
    echo Python Process:
    tasklist /FI "IMAGENAME eq python.exe" /FO TABLE
    echo.
) else (
    echo Status: NOT RUNNING (completed or crashed)
    echo.
)

REM Count dialog detections (first 50 saved)
if exist "C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\dialog_detections" (
    echo Dialog Detection Images (first 50 saved):
    dir "C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\dialog_detections\*.png" /B 2>NUL | find /C ".png"
    echo.

    echo Latest Detection:
    dir "C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\dialog_detections\*.png" /O-D /B 2>NUL | findstr /N "^" | findstr "^1:"
) else (
    echo No dialog detections folder found yet.
)

echo.
echo ================================================
echo Refreshing in 10 seconds... (Ctrl+C to exit)
echo ================================================

timeout /t 10 /nobreak >nul
goto loop
