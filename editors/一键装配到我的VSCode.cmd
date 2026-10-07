@echo off
chcp 65001 >nul
title ChinesePython 一键装配到我的 VSCode
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0attach-to-vscode.ps1" %*
echo.
pause