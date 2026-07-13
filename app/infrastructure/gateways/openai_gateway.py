import httpx

from app.application.ports import TextGenerationError
from app.infrastructure.settings import Settings


class OpenAITextGenerator:
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, prompt: str) -> str:
        if not self.settings.openai_api_key:
            raise TextGenerationError("OPENAI_API_KEY is not configured")

        try:
            response = httpx.post(
                f"{self.settings.openai_base_url}/responses",
                headers={
                    "Authorization": f"Bearer {self.settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.settings.openai_model,
                    "input": prompt,
                },
                timeout=self.settings.openai_timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise TextGenerationError("OpenAI request failed") from error

        interpretation = self._extract_text(response.json())
        if not interpretation:
            raise TextGenerationError("OpenAI response did not include text")

        return interpretation

    def is_ready(self) -> bool:
        return bool(self.settings.openai_api_key)

    def _extract_text(self, payload: dict) -> str:
        output_text = payload.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        chunks = []
        for item in payload.get("output", []):
            for content in item.get("content", []):
                text = content.get("text")
                if isinstance(text, str):
                    chunks.append(text)

        return "\n".join(chunks).strip()
