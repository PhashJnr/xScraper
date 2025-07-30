# PowerShell script to run Twitter Monitor in background
Write-Host "Starting Twitter Monitor in Background Mode..." -ForegroundColor Green
Write-Host "This will continue running when PC is locked" -ForegroundColor Yellow
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Run the monitor
try {
    python main_scraper_locked_pc.py
}
catch {
    Write-Host "Error running monitor: $_" -ForegroundColor Red
}

Write-Host "Monitor stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit" 