@echo off
echo ==============================================
echo       Deploying Blue Star AC to Vercel
echo ==============================================
echo.

cd web-dashboard
echo Running Vercel deployment...
call vercel --prod

echo.
echo ==============================================
echo  Deployment complete! Check the URL above.
echo ==============================================
pause
