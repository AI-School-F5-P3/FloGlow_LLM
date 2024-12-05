# app/core/prompts.py
from typing import Dict, Optional
from .models import Platform, ContentRequest

class PromptTemplate:
    def __init__(self, template: str):
        self.template = template
    
    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)

class ContentPromptManager:
    PLATFORM_PROMPTS = {
        Platform.BLOG: PromptTemplate("""
        Generate a professional blog post about {topic} for {audience}.
        Tone: {tone}
        
        Structure:
        1. SEO-optimized title
        2. Engaging introduction with hook
        3. 3-4 main points with subheadings
        4. Actionable conclusion
        5. Meta description
        
        Guidelines:
        - Include statistics and data when relevant
        - Use {tone} language throughout
        - Implement proper keyword density
        - Add internal linking suggestions
        - Include meta descriptions and tags
        
        Additional context: {context}
        """),
        
        Platform.TWITTER: PromptTemplate("""
        Create a Twitter thread about {topic} for {audience}.
        Tone: {tone}
        
        Thread structure:
        1. Hook tweet (Tweet 1/N)
        2. Key points (2-5 tweets)
        3. Conclusion with CTA
        
        Guidelines:
        - Each tweet under 280 characters
        - Use engaging hooks
        - Include 2-3 relevant hashtags
        - Break complex ideas across tweets
        - End with clear call-to-action
        
        Additional context: {context}
        """),
        
        Platform.INSTAGRAM: PromptTemplate("""
        Create an Instagram post about {topic} for {audience}.
        Tone: {tone}
        
        Required elements:
        1. Attention-grabbing first line
        2. Main content (max 2200 characters)
        3. Strategic line breaks
        4. Hashtag set (20-25 tags)
        
        Guidelines:
        - Start with hook before line break
        - Use emojis strategically
        - Include bullet points for readability
        - End with engagement question
        - Separate hashtags from main content
        
        Additional context: {context}
        """),
        
        Platform.LINKEDIN: PromptTemplate("""
        Create a LinkedIn post about {topic} for {audience}.
        Tone: {tone}
        
        Structure:
        1. Professional hook
        2. Industry insight/expertise
        3. Data-backed statements
        4. Professional experience tie-in
        5. Business-focused CTA
        
        Guidelines:
        - Keep under 3000 characters
        - Use professional language
        - Include industry-specific terms
        - Mention relevant trends
        - Add 3-5 professional hashtags
        
        Additional context: {context}
        """)
    }
    
    @classmethod
    def get_prompt(cls, request: ContentRequest) -> str:
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
        context = ""
        if request.brand_voice:
            context += f"\nBrand Voice Guidelines:\n"
            context += f"Company: {request.brand_voice.get('company_name')}\n"
            context += f"Tone: {request.brand_voice.get('tone')}\n"
            context += f"Values: {', '.join(request.brand_voice.get('values', []))}\n"
            context += f"Keywords: {', '.join(request.brand_voice.get('keywords', []))}"
            
            if request.brand_voice.get('style_guide'):
                context += f"\nStyle Guide: {request.brand_voice['style_guide']}"
        return context