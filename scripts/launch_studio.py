"""
PodX Studio Autonomous Launcher
Checks server health, starts uvicorn with proper PYTHONPATH if not running,
waits for health check readiness, and automatically opens the browser.
"""
import os
import sys
import time
import subprocess
import urllib.request
import webbrowser
from pathlib import Path

PORT = 8001
URL = f"http://127.0.0.1:{PORT}"
HEALTH_URL = f"{URL}/api/health"

def is_server_ready():
    try:
        req = urllib.request.Request(HEALTH_URL, headers={"User-Agent": "PodX-Launcher"})
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            return resp.status == 200
    except Exception:
        return False

def main():
    base_dir = Path(__file__).resolve().parent.parent
    os.chdir(str(base_dir))

    print("=" * 65)
    print("       PodX — Elite Knowledge AI Podcast Studio Launcher       ")
    print("=" * 65)

    if is_server_ready():
        print(f"\n[INFO] PodX Studio server is already running on {URL}.")
        print("[INFO] Launching your browser now...\n")
        webbrowser.open(URL)
        return

    print(f"\n[1/2] Initializing PodX Studio server on {URL}...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(base_dir)

    server_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "backend.main:app",
        "--host", "127.0.0.1",
        "--port", str(PORT)
    ], cwd=str(base_dir), env=env)

    # Wait up to 15 seconds for server to report ready
    ready = False
    print("[2/2] Waiting for server socket readiness...", end="", flush=True)
    for _ in range(30):
        time.sleep(0.5)
        print(".", end="", flush=True)
        if is_server_ready():
            ready = True
            break

    print()
    if ready:
        print(f"\n[SUCCESS] PodX Studio is online and healthy!")
        print(f"[INFO] Opening browser at {URL} ...\n")
        webbrowser.open(URL)
    else:
        print("\n[WARNING] Server startup took longer than expected.")
        print(f"Please open your browser manually at {URL}")

    # Keep launcher process attached to uvicorn
    try:
        server_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping PodX Studio server...")
        server_proc.terminate()

if __name__ == "__main__":
    main()
