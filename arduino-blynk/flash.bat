@echo off
cd /d "%~dp0"
echo ============================================================
echo   Flashing Blue Star AC Controller to ESP32 DevKit V1 (COM3)
echo ============================================================
echo.
pio run -t upload
if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================
    echo   SUCCESS! Firmware flashed to your ESP32.
    echo   You can now disconnect USB and wire it to your AC!
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo   Flashing failed. Please make sure the ESP32 is plugged in
    echo   and no other program (like Serial Monitor) is using COM3.
    echo ============================================================
)
echo.
pause
