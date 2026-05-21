"""
AeroSmart Full-Stack Launcher
------------------------------
Starts both servers with a single command:
  python start.py

  Backend  → http://127.0.0.1:5000  (Flask REST API)
  Frontend → http://localhost:5173   (Vite + React, opens browser automatically)
"""
import subprocess
import sys
import os
import threading
import time

ROOT     = os.path.dirname(os.path.abspath(__file__))
BACKEND  = os.path.join(ROOT, 'backend')
FRONTEND = os.path.join(ROOT, 'frontend')

# Prefer the project venv Python so Flask dependencies are available
VENV_PY  = os.path.join(ROOT, 'venv', 'Scripts', 'python.exe')
PYTHON   = VENV_PY if os.path.exists(VENV_PY) else sys.executable


def _run_backend():
    print("[Backend]  Flask API  →  http://127.0.0.1:5000")
    subprocess.run([PYTHON, 'main.py'], cwd=BACKEND)


def _run_frontend():
    # shell=True is required on Windows: npm/npx are .cmd wrappers, not binaries
    print("[Frontend] Vite dev   →  http://localhost:5173  (browser opening…)")
    subprocess.run('npm run dev', cwd=FRONTEND, shell=True)


if __name__ == '__main__':
    banner = "  AeroSmart Airlines v2.0 — Full Stack Launcher  "
    print("=" * len(banner))
    print(banner)
    print("=" * len(banner))
    print()

    bt = threading.Thread(target=_run_backend,  daemon=True, name='Backend')
    ft = threading.Thread(target=_run_frontend, daemon=True, name='Frontend')

    bt.start()
    time.sleep(1.5)   # give Flask a head start so the proxy has a target on first request
    ft.start()

    try:
        bt.join()
        ft.join()
    except KeyboardInterrupt:
        print("\n[AeroSmart] Ctrl+C received — shutting down.")
        sys.exit(0)
