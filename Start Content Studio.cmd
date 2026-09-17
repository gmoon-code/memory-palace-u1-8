@echo off
setlocal
cd /d "%~dp0"
title The Story Method - Content Studio

echo.
echo ================================================
echo   The Story Method - Content Studio
echo   Local-only zero-cost launcher
echo ================================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
  set "PYTHON_COMMAND=py -3"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set "PYTHON_COMMAND=python"
  ) else (
    echo Python was not found on this computer.
    echo Install a free Python 3 release, then double-click this file again.
    echo No account, hosting plan, billing method, or paid service is required.
    echo.
    pause
    exit /b 1
  )
)

%PYTHON_COMMAND% "%~dp0scripts\bootstrap_content_studio_windows.py"
set "CONTENT_STUDIO_EXIT=%errorlevel%"

if not "%CONTENT_STUDIO_EXIT%"=="0" (
  echo.
  echo Content Studio stopped because setup or startup did not complete.
  echo Review the message above. Nothing was published and no paid service was contacted.
  echo.
  pause
)

exit /b %CONTENT_STUDIO_EXIT%
