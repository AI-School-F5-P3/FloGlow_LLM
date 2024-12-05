from pydantic import BaseSettings
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
   """Application settings and configuration"""

   # LLM Configuration
   OLLAMA_HOST: str = "http://localhost:11434"
   OLLAMA_MODEL: str = "mistral"
   GROQ_API_KEY: str
   MODEL_NAME: str = "mixtral-8x7b-32768"
   MAX_TOKENS: int = 1000

   # Model Providers
   MODEL_PROVIDERS: Dict[str, Dict] = {
       "ollama": {
           "host": OLLAMA_HOST,
           "model": OLLAMA_MODEL
       },
       "groq": {
           "api_key": GROQ_API_KEY,
           "model": MODEL_NAME
       }
   }
   
   # App Config
   APP_NAME: str = "FlowGlow"
   APP_VERSION: str = "0.1.0"
   DEBUG: bool = False
   
   # Content Settings
   DEFAULT_LANGUAGE: str = "en"
   SUPPORTED_PLATFORMS: list = ["blog", "twitter", "instagram", "linkedin"]
   
   # Cache Config
   ENABLE_CACHE: bool = True
   CACHE_TTL: int = 3600  # 1 hour
   
   class Config:
       env_file = ".env"
       case_sensitive = True

   @classmethod
   def get_settings(cls) -> "Settings":
       """Get application settings"""
       load_dotenv()
       return cls()

settings = Settings.get_settings()