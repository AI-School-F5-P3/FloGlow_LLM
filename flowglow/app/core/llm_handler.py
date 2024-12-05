# app/core/llm_handler.py
from langchain.llms import Ollama
from groq import Groq
from typing import Optional, Dict, Any
from .config import settings
from .models import LLMResponse, ModelProvider
from datetime import datetime
import re

class LLMHandler:
    def __init__(self, provider="ollama"):
        self.provider = provider
        self.model = self._initialize_model()

    def _initialize_model(self):
        if self.provider == "ollama":
            return Ollama(
                base_url=settings.OLLAMA_HOST,
                model=settings.OLLAMA_MODEL
            )
        return Groq(
            api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME
        )

    def _init_ollama(self):
       return Ollama(
           base_url=settings.OLLAMA_HOST,
           model=settings.OLLAMA_MODEL
       )
       
    def _init_groq(self):
       return Groq(
           api_key=settings.GROQ_API_KEY,
           model=settings.MODEL_NAME
       )

async def generate(self, prompt: str) -> LLMResponse:
    try:
        response = await self.model.generate(prompt)
        processed_content = self._process_response(response)
        
        # Add response formatting
        if "Assistant:" in processed_content:
            processed_content = processed_content.split("Assistant:")[-1].strip()
        
        return LLMResponse(
            raw_response=response,
            processed_content=processed_content,
            metadata={
                "provider": self.provider,
                "model": self.model.model,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    except ConnectionError:
        return LLMResponse(
            raw_response="",
            error="Failed to connect to LLM service",
            metadata={"error_type": "connection_error"}
        )
    except Exception as e:
        return LLMResponse(
            raw_response="",
            error=str(e),
            metadata={
                "error_type": type(e).__name__,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

def _process_response(self, response: str) -> str:
    processed = response.strip()
    # Clean assistant markers
    if "Assistant:" in processed:
        processed = processed.split("Assistant:")[-1].strip()
    # Clean system prompts/artifacts
    processed = re.sub(r'<[^>]+>', '', processed)
    return processed