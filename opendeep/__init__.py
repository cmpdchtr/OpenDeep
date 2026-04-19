"""
OpenDeep
A free, unofficial client for the DeepSeek API with a Google Gemini-like syntax.
"""

from .config import configure
from .models import GenerativeModel

__version__ = "0.1.0"
__all__ = ["configure", "GenerativeModel"]
