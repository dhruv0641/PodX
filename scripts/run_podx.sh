#!/usr/bin/env bash
# ==============================================================================
# PodX - Autonomous Local AI Podcast Studio Launcher for Linux / macOS
# ==============================================================================
set -e

echo -e "\033[1;36m=================================================================\033[0m"
echo -e "\033[1;35m         PodX — Elite Knowledge AI Podcast Studio                \033[0m"
echo -e "\033[1;36m=================================================================\033[0m"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo -e "\n\033[1;33m[1/4] Auditing system hardware capabilities...\033[0m"
python3 scripts/detect_hardware.py

echo -e "\n\033[1;33m[2/4] Verifying SQLite database & 24 voice profiles...\033[0m"
python3 -c "
import sys
sys.path.insert(0, '.')
from database.db_manager import db_manager
db_manager.seed_default_voices('configs/voice_profiles.json')
voices = db_manager.get_all_voices()
print(f'Database verified: {len(voices)} active voice profiles.')
"

if [ ! -f "frontend/dist/index.html" ]; then
    echo -e "\n\033[1;33m[3/4] Building production React frontend...\033[0m"
    npm --prefix frontend run build
else
    echo -e "\n\033[1;32m[3/4] Production frontend build verified in frontend/dist.\033[0m"
fi

echo -e "\n\033[1;36m[4/4] Starting PodX Unified Server on http://127.0.0.1:8000 ...\033[0m"
echo -e "\033[1;32mAccess the Studio in your browser: http://127.0.0.1:8000\033[0m"
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
