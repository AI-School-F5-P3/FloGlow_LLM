from typing import List, Optional
import httpx
from .models import ImageGenerationRequest, ImageResponse
from .config import settings

class ImageHandler:
    """Handler for image generation and retrieval"""
    
    def __init__(self):
        self.api_base = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Client-ID {settings.UNSPLASH_API_KEY}"
        }
    
    async def get_images(self, request: ImageGenerationRequest) -> ImageResponse:
        """Get images from Unsplash"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base}/search/photos",
                    headers=self.headers,
                    params={
                        "query": request.query,
                        "per_page": request.count,
                        "orientation": "landscape"
                    }
                )
                
                if response.status_code != 200:
                    return ImageResponse(
                        urls=[],
                        error=f"API Error: {response.status_code}"
                    )
                
                data = response.json()
                urls = [img["urls"][request.size] for img in data["results"]]
                
                return ImageResponse(
                    urls=urls,
                    metadata={
                        "total_results": data["total"],
                        "query": request.query
                    }
                )
                
        except Exception as e:
            return ImageResponse(
                urls=[],
                error=str(e)
            )