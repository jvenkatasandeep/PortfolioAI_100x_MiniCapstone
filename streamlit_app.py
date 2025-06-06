from pathlib import Path
import sys
import os
import threading
import uvicorn

ROOT = Path(__file__).resolve().parent
frontend_dir = ROOT / "frontend"
src_dir = frontend_dir / "src"
sys.path.append(str(frontend_dir))
sys.path.append(str(src_dir))

# Optionally start the FastAPI backend when running on Streamlit Cloud

def _start_backend():
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("BACKEND_PORT", 8000)),
        log_level="info",
    )

if os.environ.get("START_BACKEND", "false").lower() in {"1", "true", "yes"}:
    threading.Thread(target=_start_backend, daemon=True).start()

from app import main

if __name__ == "__main__":
    main()

