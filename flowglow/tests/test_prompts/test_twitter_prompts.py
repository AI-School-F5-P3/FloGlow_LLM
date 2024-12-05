import pytest
from app.core.models import ContentRequest, Platform
from app.core.prompts import ContentPromptManager

def test_twitter_character_limit():
    request = ContentRequest(
        topic="AI Updates",
        platform=Platform.TWITTER,
        audience="tech enthusiasts",
        tone="informative"
    )
    prompt = ContentPromptManager.get_prompt(request)
    assert "280 characters" in prompt.lower()

def test_twitter_thread_structure():
    request = ContentRequest(
        topic="AI News",
        platform=Platform.TWITTER,
        audience="general public",
        tone="casual"
    )
    prompt = ContentPromptManager.get_prompt(request)
    assert all(x in prompt.lower() for x in ["thread", "hashtags"])