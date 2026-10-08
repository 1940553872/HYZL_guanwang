@echo off
rem Open the HYZL website static demo (needs Node.js 18+).
chcp 65001 >nul
cd /d "%~dp0"
node demo-server.mjs
pause
