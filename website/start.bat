@echo off
rem One-click start for the HYZL website (Windows). Add -Rebuild to force a rebuild.
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0hyzl.ps1" start %*
pause
