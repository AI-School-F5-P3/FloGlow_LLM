# app/core/llm_handler.py
from langchain_community.llms.ollama import Ollama
from groq import Groq
import httpx
from typing import Optional, Dict, Any, Tuple, List
from .config import settings
from .models import LLMResponse, ModelProvider, ImageParams
from datetime import datetime
import re

class LLMHandler:
    def __init__(self, provider="ollama"):
        self.provider = provider
        self.model = self._initialize_model()
        self.unsplash_api_url = "https://api.unsplash.com/search/photos"
        self.unsplash_headers = {
            "Authorization": f"Client-ID {settings.UNSPLASH_API_KEY}"
        }
        self.image_cache = {}  # Simple cache for images

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

    async def get_image(self, 
                       query: str, 
                       size: str = "regular", 
                       orientation: str = "landscape") -> Optional[Dict[str, Any]]:
        """Get relevant image from Unsplash with specific parameters"""
        cache_key = f"{query}_{size}_{orientation}"
        
        # Check cache first
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.unsplash_api_url,
                    headers=self.unsplash_headers,
                    params={
                        "query": query,
                        "per_page": 1,
                        "orientation": orientation
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data["results"]:
                        image_data = {
                            "url": data["results"][0]["urls"][size],
                            "author": data["results"][0]["user"]["name"],
                            "description": data["results"][0]["description"] or data["results"][0]["alt_description"],
                            "download_location": data["results"][0]["links"]["download_location"]
                        }
                        # Cache the result
                        self.image_cache[cache_key] = image_data
                        # Trigger download count (Unsplash requirement)
                        await self._trigger_download_count(image_data["download_location"])
                        return image_data
                elif response.status_code == 403:
                    raise Exception("Unsplash API key invalid or rate limit exceeded")
                return None
        except httpx.RequestError as e:
            print(f"Network error fetching image: {str(e)}")
            return None
        except Exception as e:
            print(f"Error fetching image: {str(e)}")
            return None

    async def _trigger_download_count(self, download_location: str):
        """Trigger Unsplash download count (required by API guidelines)"""
        try:
            async with httpx.AsyncClient() as client:
                await client.get(
                    download_location,
                    headers=self.unsplash_headers
                )
        except Exception as e:
            print(f"Error triggering download count: {str(e)}")

    async def generate(self, 
                      prompt: str, 
                      include_image: bool = False,
                      image_params: Optional[Dict[str, str]] = None) -> Tuple[str, Optional[Dict[str, Any]]]:
        try:
            # Generate text content
            if self.provider == "ollama":
                response = await self.model.agenerate([prompt])
                content = response.generations[0][0].text
            else:
                response = await self.model.generate(prompt)
                content = response

            processed_content = self._process_response(content)
            
            # Get image if requested
            image_data = None
            if include_image:
                # Extract keywords for image search
                keywords = " ".join(processed_content.split()[:5])
                image_params = image_params or {}
                image_data = await self.get_image(
                    query=keywords,
                    size=image_params.get("size", "regular"),
                    orientation=image_params.get("orientation", "landscape")
                )
            
            return processed_content, image_data
            
        except ConnectionError as e:
            return f"Connection Error: {str(e)}", None
        except Exception as e:
            return f"Error: {str(e)}", None

    def _process_response(self, response: str) -> str:
        if not isinstance(response, str):
            response = str(response)
            
        processed = response.strip()
        if "Assistant:" in processed:
            processed = processed.split("Assistant:")[-1].strip()
        processed = re.sub(r'<[^>]+>', '', processed)
        return processed

    async def generate_with_metadata(self, 
                                   prompt: str, 
                                   include_image: bool = False,
                                   image_params: Optional[Dict[str, str]] = None) -> LLMResponse:
        try:
            content, image_data = await self.generate(prompt, include_image, image_params)
            return LLMResponse(
                raw_response=content,
                processed_content=content,
                image_data=image_data,
                metadata={
                    "provider": self.provider,
                    "model": self.model.model_name if hasattr(self.model, 'model_name') else settings.MODEL_NAME,
                    "timestamp": datetime.utcnow().isoformat(),
                    "has_image": bool(image_data)
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