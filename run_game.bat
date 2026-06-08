@echo off
echo Checking if pygame is installed...
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pygame is not installed. Installing it now...
    python -m pip install pygame
) else (
    echo Pygame is already installed.
)
echo Starting the game...
python Game.py
pause
