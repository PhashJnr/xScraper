@echo off
echo Starting Twitter Monitor in Background Mode...
echo This will continue running when PC is locked
echo.
echo Press Ctrl+C to stop the monitor
echo.

cd /d "%~dp0"
python main_scraper_locked_pc.py

pause 