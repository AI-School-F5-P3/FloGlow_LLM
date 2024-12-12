from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # LLM Configuration
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"
    GROQ_API_KEY: str = "apikey"  
    MODEL_NAME: str = "mixtral-8x7b-32768"
    MAX_TOKENS: int = 1000
    
    # Model Providers Configuration
    MODEL_PROVIDERS: Dict[str, Dict] = {
        "ollama": {
            "host": "http://localhost:11434",
            "model": "mistral"
        },
        "groq": {
            "api_key": GROQ_API_KEY,
            "model": "mixtral-8x7b-32768"
        }
    }
    
    # Application Configuration
    APP_NAME: str = "FlowGlow"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    UNSPLASH_API_KEY: str = Field(..., description="Unsplash API key for image fetching")
    
    # Content Generation Settings
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_PLATFORMS: list = ["blog", "twitter", "instagram", "linkedin"]
    
    # Cache Configuration
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    
    # LLM Default Settings
    DEFAULT_PROVIDER: str = "ollama"
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = ""  # No prefix for environment variables
        
    @classmethod
    def get_settings(cls) -> "Settings":
        """Get application settings with environment variables loaded"""
        load_dotenv(override=True)  # Added override to ensure env vars are loaded
        return cls()

    def get_model_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for specific model provider"""
        return self.MODEL_PROVIDERS.get(provider, self.MODEL_PROVIDERS[self.DEFAULT_PROVIDER])

settings = Settings.get_settings()