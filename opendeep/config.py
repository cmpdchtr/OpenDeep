from dataclasses import dataclass
from typing import Optional

@dataclass
class Configuration:
    """Global configuration settings for the OpenDeep client."""
    api_key: Optional[str] = None
    base_url: str = "https://chat.deepseek.com/api/v0"
    user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

config = Configuration()

def configure(api_key: Optional[str] = None, **kwargs) -> None:
    """
    Configures the global parameters for the OpenDeep client.
    
    Args:
        api_key: The userToken from the chat.deepseek.com localStorage.
        **kwargs: Additional configuration parameters (e.g., base_url, user_agent).
    """
    if api_key:
        config.api_key = api_key
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
