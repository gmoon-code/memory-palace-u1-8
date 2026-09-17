@echo off
setlocal
cd /d "%~dp0"

echo The Story Method - Content Studio Repair
echo ----------------------------------------
echo This repair is local-only and uses no paid service, hosting plan, API, or billing account.
echo Content Studio must be stopped before repair begins.
echo.

set "PYTHON_CMD="
where py >nul 2>&1
if %errorlevel%==0 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD (
  where python >nul 2>&1
  if %errorlevel%==0 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  echo ERROR: Python 3 was not found.
  echo Install a current free Python 3 release, then run this file again.
  pause
  exit /b 1
)

%PYTHON_CMD% scripts\repair_content_studio_local.py %*
set "RESULT=%errorlevel%"

if not "%RESULT%"=="0" (
  echo.
  echo Repair did not complete. Review the message above.
  pause
  exit /b %RESULT%
)

echo.
echo Repair completed successfully.
echo You can now double-click Start Content Studio.cmd.
pause
exit /b 0
