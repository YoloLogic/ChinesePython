@echo off
chcp 65001 >nul
title ChinesePython 一键还原
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0detach-from-vscode.ps1" %*
echo.
pause