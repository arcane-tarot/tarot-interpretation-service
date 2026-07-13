from dataclasses import dataclass

from app.domain.models import TarotCard


@dataclass(frozen=True)
class InterpretTarotCardCommand:
    question: str
    deck_type: str
    card: TarotCard
