@echo off
setlocal
cd /d "%~dp0"
title The Story Method - Content Studio Update

echo.
echo ================================================
echo   The Story Method - Content Studio Update
echo   Validated local-only zero-cost updater
echo ================================================
echo.
echo Close Content Studio before continuing.
echo The updater will refuse unvalidated or non-fast-forward code.
echo A local state backup is created before any code update.
echo.

set "PYTHON_COMMAND="
where py >nul 2>nul
if not errorlevel 1 set "PYTHON_COMMAND=py -3"
if not defined PYTHON_COMMAND (
  where python >nul 2>nul
  if not errorlevel 1 set "PYTHON_COMMAND=python"
)
if not defined PYTHON_COMMAND if exist "%~dp0.venv\Scripts\python.exe" set "PYTHON_COMMAND=%~dp0.venv\Scripts\python.exe"

if not defined PYTHON_COMMAND (
  echo Python was not found on this computer.
  echo The updater made no changes.
  echo Install a free Python 3 release or continue using the current Content Studio.
  echo No account, billing method, or paid service is required.
  echo.
  pause
  exit /b 1
)

%PYTHON_COMMAND% "%~dp0scripts\update_content_studio_local.py"
set "UPDATE_EXIT=%errorlevel%"

echo.
if "%UPDATE_EXIT%"=="0" (
  echo Update check finished successfully.
) else (
  echo Content Studio was not left on an unvalidated update.
  echo Review the message above. Existing local state backups were preserved.
)
echo.
pause
exit /b %UPDATE_EXIT%
