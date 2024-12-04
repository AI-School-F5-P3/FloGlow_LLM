from typing import Dict, Optional
from .models import Platform, ContentRequest

class PromptTemplate:
    """Base prompt template class"""
    def __init__(self, template: str):
        self.template = template
    
    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)

class ContentPromptManager:
    """Manager for content generation prompts"""
    
    PLATFORM_PROMPTS = {
        Platform.BLOG: PromptTemplate("""
        Create a blog post about {topic} for {audience}.
        Tone: {tone}
        
        Guidelines:
        - Create an engaging headline
        - Write a compelling introduction
        - Include 3-4 main points
        - Add a strong conclusion
        - Use SEO-friendly subheadings
        - Maintain {tone} tone throughout
        - Include relevant keywords
        
        Additional context: {context}
        """),
        
        Platform.TWITTER: PromptTemplate("""
        Create a Twitter thread about {topic} for {audience}.
        Tone: {tone}
        
        Guidelines:
        - First tweet should be attention-grabbing
        - Break down information into 280-character tweets
        - Use engaging language
        - Include relevant hashtags
        - End with a call to action
        
        Additional context: {context}
        """),
        
        # Add other platform templates...
    }
    
    @classmethod
    def get_prompt(cls, request: ContentRequest) -> str:
        """Get formatted prompt for content generation"""
        template = cls.PLATFORM_PROMPTS.get(request.platform)
        if not template:
            raise ValueError(f"No template found for platform: {request.platform}")
        
        return template.format(
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            context=cls._get_additional_context(request)
        )
    
    @staticmethod
    def _get_additional_context(request: ContentRequest) -> str:
        """Generate additional context based on request"""
        # Add platform-specific context logic here
        return ""