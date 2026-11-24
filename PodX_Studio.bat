@echo off
title PodX - Elite Knowledge AI Podcast Studio
cd /d "D:\Dhruv\PodX"

echo =================================================================
echo          PodX -- Elite Knowledge AI Podcast Studio
echo =================================================================
echo.
echo Starting PodX Studio Server on http://127.0.0.1:8001 ...
echo Opening your default browser...

start "" "http://127.0.0.1:8001"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001

pause
