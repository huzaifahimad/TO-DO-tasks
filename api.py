import sys
from pathlib import Path

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok", "service": "TODO API"}

# Export the app for Vercel
__all__ = ['app']
