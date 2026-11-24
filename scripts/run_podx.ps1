# ==============================================================================
# PodX - Autonomous Local AI Podcast Studio Launcher for Windows (PowerShell)
# ==============================================================================
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "         PodX — Elite Knowledge AI Podcast Studio                " -ForegroundColor Magenta
Write-Host "=================================================================" -ForegroundColor Cyan

$baseDir = Split-Path -Parent $PSScriptRoot
Set-Location $baseDir

# 1. Hardware Audit
Write-Host "`n[1/4] Auditing system hardware capabilities..." -ForegroundColor Yellow
python scripts\detect_hardware.py

# 2. Database Schema and Voices Check
Write-Host "`n[2/4] Initializing SQLite database and verifying 24 voice profiles..." -ForegroundColor Yellow
python -c "
import sys
sys.path.insert(0, '.')
from database.db_manager import db_manager
db_manager.seed_default_voices('configs/voice_profiles.json')
voices = db_manager.get_all_voices()
print(f'Database verified: {len(voices)} active voice profiles.')
"

# 3. Build Frontend if needed
if (-not (Test-Path "frontend\dist\index.html")) {
    Write-Host "`n[3/4] Building production React frontend..." -ForegroundColor Yellow
    npm --prefix frontend run build
} else {
    Write-Host "`n[3/4] Production frontend build verified in frontend\dist." -ForegroundColor Green
}

# 4. Start Server
Write-Host "`n[4/4] Starting PodX Unified Server on http://127.0.0.1:8001 ..." -ForegroundColor Cyan
Write-Host "Access the Studio in your browser: http://127.0.0.1:8001" -ForegroundColor Green
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001
