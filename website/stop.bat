@echo off
rem One-click stop for the HYZL website (Windows).
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0hyzl.ps1" stop
pause
