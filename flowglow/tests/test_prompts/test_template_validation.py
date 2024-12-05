import pytest
from app.core.prompts import ContentPromptManager
from app.core.models import ContentRequest, Platform

def test_template_existence():
    for platform in Platform:
        template = ContentPromptManager.PLATFORM_PROMPTS.get(platform)
        assert template is not None

def test_template_formatting():
    request = ContentRequest(
        topic="Test",
        platform=Platform.BLOG,
        audience="testers"
    )
    prompt = ContentPromptManager.get_prompt(request)
    assert request.topic in prompt
    assert request.audience in prompt