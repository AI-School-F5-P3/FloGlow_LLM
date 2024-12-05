import pytest
from app.utils.validators import ContentValidator
from app.core.models import Platform

def test_length_validation():
    content = "x" * 281
    valid, message = ContentValidator.validate_content(content, Platform.TWITTER)
    assert not valid
    assert "length" in message.lower()

def test_content_quality():
    spam_content = "Buy now! Special offer! Discount!"
    valid, message = ContentValidator.validate_content(spam_content, Platform.BLOG)
    assert not valid
    assert "quality" in message.lower()