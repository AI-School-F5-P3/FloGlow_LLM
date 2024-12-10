# app/core/llm_handler.py
from langchain_community.llms.ollama import Ollama
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
        providers = {
            "ollama": self._init_ollama,
            "groq": self._init_groq
        }
        return providers[self.provider]()

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

    async def generate(self, prompt: str) -> str:  # Changed return type to str
        try:
            # Different handling for different providers
            if self.provider == "ollama":
                response = await self.model.agenerate([prompt])
                content = response.generations[0][0].text
            else:
                response = await self.model.generate(prompt)
                content = response

            processed_content = self._process_response(content)
            
            # Return processed content directly
            return processed_content
            
        except ConnectionError as e:
            return f"Connection Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _process_response(self, response: str) -> str:
        if not isinstance(response, str):
            response = str(response)
            
        processed = response.strip()
        # Clean assistant markers
        if "Assistant:" in processed:
            processed = processed.split("Assistant:")[-1].strip()
        # Clean system prompts/artifacts
        processed = re.sub(r'<[^>]+>', '', processed)
        return processed

    async def generate_with_metadata(self, prompt: str) -> LLMResponse:
        """Generate content with full metadata"""
        try:
            content = await self.generate(prompt)
            return LLMResponse(
                raw_response=content,
                processed_content=content,
                metadata={
                    "provider": self.provider,
                    "model": self.model.model_name if hasattr(self.model, 'model_name') else settings.MODEL_NAME,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            return LLMResponse(
                raw_response="",
                processed_content="",
                error=str(e),
                metadata={
                    "error_type": type(e).__name__,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )