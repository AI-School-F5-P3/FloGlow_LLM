from typing import Dict, Optional, Tuple
from app.core.models import ContentRequest, ContentType, Platform
import re

class ContentValidator:
    """Validator for content generation requests and responses"""
    
    PLATFORM_LIMITS = {
        Platform.TWITTER: 280,
        Platform.INSTAGRAM: 2200,
        Platform.LINKEDIN: 3000,
        Platform.BLOG: 100000
    }
    
    @classmethod
    def validate_request(cls, request: ContentRequest) -> Tuple[bool, Optional[str]]:
        """Validate content generation request"""
        # Validate topic
        if not request.topic or len(request.topic.strip()) < 3:
            return False, "Topic must be at least 3 characters long"
            
        # Validate audience
        if not request.audience or len(request.audience.strip()) < 3:
            return False, "Audience description must be at least 3 characters long"
            
        # Validate platform-specific requirements
        platform_validator = getattr(cls, f"_validate_{request.platform.lower()}", None)
        if platform_validator:
            valid, message = platform_validator(request)
            if not valid:
                return False, message
                
        return True, None
    
    @classmethod
    def validate_content(cls, content: str, platform: Platform) -> Tuple[bool, Optional[str]]:
        """Validate generated content"""
        # Check content length
        max_length = cls.PLATFORM_LIMITS.get(platform)
        if max_length and len(content) > max_length:
            return False, f"Content exceeds maximum length for {platform}"
            
        # Check for prohibited content
        if cls._contains_prohibited_content(content):
            return False, "Content contains prohibited elements"
            
        return True, None
    
    @staticmethod
    def _validate_twitter(request: ContentRequest) -> Tuple[bool, Optional[str]]:
        """Twitter-specific validation"""
        if request.content_type == ContentType.IMAGE and not request.topic:
            return False, "Image tweets require a text description"
        return True, None
    
    @staticmethod
    def _validate_instagram(request: ContentRequest) -> Tuple[bool, Optional[str]]:
        """Instagram-specific validation"""
        if request.content_type == ContentType.TEXT:
            return False, "Instagram posts require at least one image"
        return True, None
    
    @staticmethod
    def _contains_prohibited_content(content: str) -> bool:
        """Check for prohibited content patterns"""
        prohibited_patterns = [
            r'(?i)spam',
            r'(?i)abuse',
            r'(?i)explicit',
            # Add more patterns as needed
        ]
        
        return any(re.search(pattern, content) for pattern in prohibited_patterns)