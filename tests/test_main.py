from fastapi.testclient import TestClient

from app.application.ports import TextGenerationError
from app.application.use_cases.interpret_tarot_card import (
    InterpretTarotCardUseCase,
)
from app.bootstrap import get_interpret_tarot_card_use_case, get_text_generator
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "question": "Que necesito entender sobre esta decision?",
    "deckType": "major",
    "card": {
        "name": "El Mago",
        "type": "major",
        "label": "Arcano mayor",
        "baseMeaning": "Voluntad, recursos y accion enfocada.",
    },
}


class FakeTextGenerator:
    def __init__(
        self,
        text="Una interpretacion contextual.",
        ready=True,
        error=None,
    ):
        self.text = text
        self.ready = ready
        self.error = error
        self.prompts = []

    def generate(self, prompt: str) -> str:
        if self.error is not None:
            raise self.error
        self.prompts.append(prompt)
        return self.text

    def is_ready(self) -> bool:
        return self.ready


def setup_function():
    app.dependency_overrides.clear()


def teardown_function():
    app.dependency_overrides.clear()


def test_interpretation_returns_contextual_reading():
    generator = FakeTextGenerator("El Mago pide convertir intuicion en accion.")
    use_case = InterpretTarotCardUseCase(generator)
    app.dependency_overrides[get_interpret_tarot_card_use_case] = lambda: use_case

    response = client.post("/api/tarot/interpretations", json=VALID_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {
        "cardName": "El Mago",
        "interpretation": "El Mago pide convertir intuicion en accion.",
    }
    assert "Pregunta: Que necesito entender" in generator.prompts[0]
    assert "Carta: El Mago" in generator.prompts[0]


def test_interpretation_returns_503_when_openai_fails():
    generator = FakeTextGenerator(error=TextGenerationError("OpenAI unavailable"))
    app.dependency_overrides[get_interpret_tarot_card_use_case] = (
        lambda: InterpretTarotCardUseCase(generator)
    )

    response = client.post("/api/tarot/interpretations", json=VALID_PAYLOAD)

    assert response.status_code == 503
    assert response.json() == {"detail": "OpenAI unavailable"}


def test_interpretation_rejects_invalid_payload():
    payload = {**VALID_PAYLOAD, "question": ""}

    response = client.post("/api/tarot/interpretations", json=payload)

    assert response.status_code == 422


def test_metrics_are_exposed_at_conventional_path():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "tarot_http_requests_total" in response.text
    assert "tarot_http_request_duration_seconds" in response.text


def test_metrics_are_not_exposed_under_tarot_api():
    response = client.get("/api/tarot/metrics")

    assert response.status_code == 404


def test_health_probes_ready():
    generator = FakeTextGenerator(ready=True)
    app.dependency_overrides[get_text_generator] = lambda: generator

    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/health/live").json() == {"status": "alive"}
    assert client.get("/health/startup").json() == {"status": "started"}

    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {"openai_api_key": "configured"},
    }


def test_readiness_returns_503_without_openai_key():
    generator = FakeTextGenerator(ready=False)
    app.dependency_overrides[get_text_generator] = lambda: generator

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "checks": {"openai_api_key": "missing"},
    }
