@echo off
echo Pushing Bluestar-SMART to GitHub...
git push -u origin main
if %ERRORLEVEL% equ 0 (
    echo.
    echo ==============================================
    echo  Successfully pushed to GitHub!
    echo ==============================================
) else (
    echo.
    echo ==============================================
    echo  Push failed! Please ensure you created the repo:
    echo  https://github.com/new?name=Bluestar-SMART
    echo ==============================================
)
pause
