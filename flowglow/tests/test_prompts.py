import pytest
from app.core.models import ContentRequest, Platform
from app.core.prompts import ContentPromptManager

def test_blog_prompt_generation():
    request = ContentRequest(
        topic="AI Technology",
        platform=Platform.BLOG,
        audience="tech professionals",
        tone="professional"
    )
    prompt = ContentPromptManager.get_prompt(request)
    assert "AI Technology" in prompt
    assert "tech professionals" in prompt