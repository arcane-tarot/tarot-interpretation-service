from app.application.use_cases.interpret_tarot_card import (
    InterpretTarotCardUseCase,
)
from app.infrastructure.gateways.openai_gateway import OpenAITextGenerator
from app.infrastructure.settings import settings

text_generator = OpenAITextGenerator(settings)


def get_text_generator() -> OpenAITextGenerator:
    return text_generator


def get_interpret_tarot_card_use_case() -> InterpretTarotCardUseCase:
    return InterpretTarotCardUseCase(text_generator=get_text_generator())
