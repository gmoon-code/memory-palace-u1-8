@echo off
setlocal
cd /d "%~dp0"
title The Story Method - Content Studio Restore

echo.
echo ================================================
echo   The Story Method - Content Studio Restore
echo   Validated local-only restore
echo ================================================
echo.
echo Close Content Studio before restoring a backup.
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

if "%~1"=="" (
  "%PYTHON_EXE%" %PYTHON_ARGS% "%~dp0scripts\restore_content_studio_local.py"
) else (
  "%PYTHON_EXE%" %PYTHON_ARGS% "%~dp0scripts\restore_content_studio_local.py" "%~1"
)
set "RESTORE_EXIT=%errorlevel%"
echo.
if "%RESTORE_EXIT%"=="0" (
  echo Restore finished successfully.
) else (
  echo Restore did not complete. Review the message above.
)
echo.
pause
exit /b %RESTORE_EXIT%
