@echo off
setlocal
cd /d "%~dp0"
title The Story Method - Content Studio Installer

echo.
echo ================================================
echo   The Story Method - Content Studio Installer
echo   Free local Windows installation
echo ================================================
echo.

where py >nul 2>nul
if not errorlevel 1 (
  py -3 "%~dp0install_content_studio.py"
  set "INSTALL_EXIT=%errorlevel%"
  goto :finished
)

where python >nul 2>nul
if not errorlevel 1 (
  python "%~dp0install_content_studio.py"
  set "INSTALL_EXIT=%errorlevel%"
  goto :finished
)

echo Python 3 was not found on this computer.
echo Install a free Python 3.10 or newer release and run this installer again.
echo Git is also required. The installer never purchases or enrolls you in a paid service.
set "INSTALL_EXIT=1"

:finished
if not "%INSTALL_EXIT%"=="0" (
  echo.
  echo Installation did not complete. Existing Content Studio data was not overwritten.
)
echo.
pause
exit /b %INSTALL_EXIT%
