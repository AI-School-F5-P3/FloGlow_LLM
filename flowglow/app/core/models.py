from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class Platform(str, Enum):
    BLOG = "blog"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"

class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    MIXED = "mixed"

class ModelProvider(str, Enum):
    OLLAMA = "ollama"
    GROQ = "groq"

class LLMConfig(BaseModel):
    model_name: str
    model_type: str = Field(..., description="local or api")
    max_tokens: int = 1024
    temperature: float = 0.7
    api_key: Optional[str] = None

class LLMProvider(BaseModel):
    name: ModelProvider
    config: LLMConfig
    active: bool = True

class BrandVoice(BaseModel):
    company_name: str
    tone: str
    values: List[str]
    keywords: List[str]
    style_guide: Optional[Dict[str, Any]] = None

class ImageRequest(BaseModel):
    query: str
    size: str = "medium"
    count: int = 1
    source: str = "unsplash"

class ContentRequest(BaseModel):
    topic: str = Field(..., description="Main topic for content generation")
    platform: Platform = Field(..., description="Target platform")
    audience: str = Field(..., description="Target audience")
    tone: str = Field(default="professional", description="Content tone")
    language: str = Field(default="en", description="Content language")
    content_type: ContentType = Field(default=ContentType.TEXT)
    brand_voice: Optional[Dict[str, Any]] = None
    
    class Config:
        use_enum_values = True

class ContentResponse(BaseModel):
    content: str
    platform: Platform
    metadata: Dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class LLMResponse(BaseModel):
    raw_response: str
    processed_content: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)