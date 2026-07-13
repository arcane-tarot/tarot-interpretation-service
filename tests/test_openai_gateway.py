import httpx
import pytest

from app.application.ports import TextGenerationError
from app.infrastructure.gateways.openai_gateway import OpenAITextGenerator
from app.infrastructure.settings import Settings


def test_openai_gateway_extracts_output_text(monkeypatch):
    settings = Settings(openai_api_key="test-key")
    generator = OpenAITextGenerator(settings)

    def fake_post(url, headers, json, timeout):
        assert url == "https://api.openai.com/v1/responses"
        assert headers["Authorization"] == "Bearer test-key"
        assert json["input"] == "prompt"
        return httpx.Response(
            status_code=200,
            json={"output_text": "Lectura lista."},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    assert generator.generate("prompt") == "Lectura lista."


def test_openai_gateway_extracts_nested_content(monkeypatch):
    settings = Settings(openai_api_key="test-key")
    generator = OpenAITextGenerator(settings)

    def fake_post(url, headers, json, timeout):
        return httpx.Response(
            status_code=200,
            json={
                "output": [
                    {
                        "content": [
                            {"type": "output_text", "text": "Parte uno."},
                            {"type": "output_text", "text": "Parte dos."},
                        ]
                    }
                ]
            },
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    assert generator.generate("prompt") == "Parte uno.\nParte dos."


def test_openai_gateway_requires_api_key():
    generator = OpenAITextGenerator(Settings(openai_api_key=""))

    with pytest.raises(TextGenerationError, match="OPENAI_API_KEY"):
        generator.generate("prompt")
