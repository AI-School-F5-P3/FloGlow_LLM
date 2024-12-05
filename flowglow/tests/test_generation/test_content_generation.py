import pytest
from app.core.models import ContentRequest, Platform
from app.core.prompts import ContentPromptManager
from app.utils.validators import ContentValidator

def test_content_generation():
    request = ContentRequest(
        topic="FlowGlow Features",
        platform=Platform.BLOG,
        audience="marketers",
        tone="professional"
    )
    content = ContentPromptManager.generate_content(request)
    valid, _ = ContentValidator.validate_content(content, Platform.BLOG)
    assert valid

def test_generation_with_brand_voice():
    request = ContentRequest(
        topic="AI Tools",
        platform=Platform.BLOG,
        audience="business",
        tone="professional",
        brand_voice="innovative"
    )
    content = ContentPromptManager.generate_content(request)
    assert "innovative" in content.lower()