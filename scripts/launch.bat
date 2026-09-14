@echo off
title Recording Menu
color 0A

:menu
cls
echo ==================================
echo          RECORDING MENU
echo ==================================
echo.
echo   [R] Start Recording
echo   [P] Play Recording
echo   [E] Exit
echo.
echo ==================================
echo.

choice /c RPE /n /m "Press R, P, or E: "

if errorlevel 3 goto exit
if errorlevel 2 goto play
if errorlevel 1 goto record

:record
cls
echo ==================================
echo          START RECORDING
echo ==================================
echo.
python record.py
echo.
echo Recording script finished.
pause
goto menu

:play
cls
echo ==================================
echo           PLAY RECORDING
echo ==================================
echo.
python play.py
echo.
echo Playback script finished.
pause
goto menu

:exit
cls
echo Exiting...
timeout /t 1 /nobreak >nul
exit
