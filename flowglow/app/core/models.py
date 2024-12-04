from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum

class Platform(str, Enum):
    """Supported social media platforms"""
    BLOG = "blog"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"

class ContentType(str, Enum):
    """Types of content that can be generated"""
    TEXT = "text"
    IMAGE = "image"
    MIXED = "mixed"

class ContentRequest(BaseModel):
    """Content generation request model"""
    topic: str = Field(..., description="Main topic for content generation")
    platform: Platform = Field(..., description="Target platform")
    audience: str = Field(..., description="Target audience")
    tone: str = Field(default="professional", description="Content tone")
    language: str = Field(default="en", description="Content language")
    content_type: ContentType = Field(default=ContentType.TEXT)
    
    class Config:
        use_enum_values = True

class ContentResponse(BaseModel):
    """Content generation response model"""
    content: str
    platform: Platform
    metadata: Dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class LLMResponse(BaseModel):
    """Raw LLM response model"""
    raw_response: str
    processed_content: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)