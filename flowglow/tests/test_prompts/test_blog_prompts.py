import pytest
from app.core.models import ContentRequest, Platform, ContentType
from app.core.prompts import ContentPromptManager

def test_blog_basic_prompt():
    request = ContentRequest(
        topic="AI Technology",
        platform=Platform.BLOG,
        audience="tech professionals",
        tone="professional"
    )
    prompt = ContentPromptManager.get_prompt(request)
    assert all(x in prompt for x in ["AI Technology", "tech professionals", "professional"])

def test_blog_structure_elements():
    request = ContentRequest(
        topic="Data Science",
        platform=Platform.BLOG,
        audience="beginners",
        tone="educational"
    )
    prompt = ContentPromptManager.get_prompt(request)
    assert all(x in prompt.lower() for x in ["introduction", "conclusion", "main points"])