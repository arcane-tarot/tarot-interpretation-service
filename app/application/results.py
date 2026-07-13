from dataclasses import dataclass


@dataclass(frozen=True)
class TarotInterpretationResult:
    card_name: str
    interpretation: str
