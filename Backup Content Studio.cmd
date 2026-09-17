@echo off
setlocal
cd /d "%~dp0"
title The Story Method - Content Studio Backup

echo.
echo ================================================
echo   The Story Method - Content Studio Backup
echo   Local-only zero-cost backup
echo ================================================
echo.

set "PYTHON_EXE="
set "PYTHON_ARGS="
if exist "%~dp0.venv\Scripts\python.exe" (
  set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
  where py >nul 2>nul
  if not errorlevel 1 (
    set "PYTHON_EXE=py"
    set "PYTHON_ARGS=-3"
  )
)
if not defined PYTHON_EXE (
  where python >nul 2>nul
  if not errorlevel 1 set "PYTHON_EXE=python"
)
if not defined PYTHON_EXE (
  echo Python was not found on this computer.
  echo Start Content Studio once first, or install a free Python 3 release.
  echo.
  pause
  exit /b 1
)

"%PYTHON_EXE%" %PYTHON_ARGS% "%~dp0scripts\backup_content_studio_local.py"
set "BACKUP_EXIT=%errorlevel%"
echo.
if "%BACKUP_EXIT%"=="0" (
  echo Backup finished successfully.
) else (
  echo Backup did not complete. Existing Content Studio data was not changed.
)
echo.
pause
exit /b %BACKUP_EXIT%
