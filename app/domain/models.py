from dataclasses import dataclass


@dataclass(frozen=True)
class TarotCard:
    name: str
    type: str
    label: str
    base_meaning: str


@dataclass(frozen=True)
class TarotQuestion:
    question: str
    deck_type: str
    card: TarotCard


@dataclass(frozen=True)
class TarotInterpretation:
    question: str
    card_name: str
    interpretation: str
