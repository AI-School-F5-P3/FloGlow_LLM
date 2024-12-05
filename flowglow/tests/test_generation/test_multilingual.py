import pytest
from app.core.models import ContentRequest, Platform
from app.core.prompts import ContentPromptManager

def test_multilingual_generation():
    languages = ["en", "es", "fr", "it"]
    for lang in languages:
        request = ContentRequest(
            topic="AI Technology",
            platform=Platform.BLOG,
            audience="general",
            tone="casual",
            language=lang
        )
        content = ContentPromptManager.generate_content(request)
        assert content != ""