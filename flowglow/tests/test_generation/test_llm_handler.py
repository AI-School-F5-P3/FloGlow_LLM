import pytest
from app.core.llm_handler import LLMHandler
from app.core.models import ModelProvider, LLMResponse

@pytest.fixture
def llm_handler():
    return LLMHandler()

async def test_ollama_initialization(llm_handler):
    assert llm_handler.provider == ModelProvider.OLLAMA
    assert llm_handler.model is not None

async def test_model_switching():
    handler = LLMHandler(provider=ModelProvider.GROQ)
    assert handler.provider == ModelProvider.GROQ

async def test_response_generation(llm_handler):
    prompt = "Generate a test response"
    response = await llm_handler.generate(prompt)
    assert isinstance(response, LLMResponse)
    assert response.error is None

async def test_error_handling(llm_handler):
    prompt = None  # Invalid prompt
    response = await llm_handler.generate(prompt)
    assert response.error is not None