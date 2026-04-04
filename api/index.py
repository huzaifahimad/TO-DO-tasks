import sys
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from main import app
except Exception as e:
    print(f"Error loading app: {e}", file=sys.stderr)
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def error_root():
        return JSONResponse({"error": "Failed to load application"}, status_code=500)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Export the app for Vercel
__all__ = ['app']
