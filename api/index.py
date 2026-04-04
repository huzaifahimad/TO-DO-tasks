import sys
from pathlib import Path

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

# Export the app for Vercel
__all__ = ['app']
