"""
OpenDeep
A free, unofficial client for the DeepSeek API with a Google Gemini-like syntax.
"""

from .config import configure
from .models import GenerativeModel, ChatSession, AsyncGenerativeModel, AsyncChatSession

__version__ = "0.9.0"
__all__ = ["configure", "GenerativeModel", "ChatSession", "AsyncGenerativeModel", "AsyncChatSession"]
