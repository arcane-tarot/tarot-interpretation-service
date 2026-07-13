from app.application.commands import InterpretTarotCardCommand
from app.application.ports import TextGenerator
from app.application.results import TarotInterpretationResult


class InterpretTarotCardUseCase:
    def __init__(self, text_generator: TextGenerator):
        self.text_generator = text_generator

    def execute(
        self,
        command: InterpretTarotCardCommand,
    ) -> TarotInterpretationResult:
        prompt = self._build_prompt(command)
        interpretation = self.text_generator.generate(prompt)

        return TarotInterpretationResult(
            card_name=command.card.name,
            interpretation=interpretation,
        )

    def _build_prompt(self, command: InterpretTarotCardCommand) -> str:
        return "\n".join(
            [
                "Eres una lectora de tarot clara, compasiva y practica.",
                "Interpreta una sola carta en el contexto de la pregunta.",
                (
                    "No predigas certezas absolutas ni des consejos medicos, "
                    "legales o financieros."
                ),
                "Responde en espanol, con 2 parrafos breves y accionables.",
                "",
                f"Pregunta: {command.question}",
                f"Tipo de mazo seleccionado: {command.deck_type}",
                f"Carta: {command.card.name}",
                f"Tipo de carta: {command.card.label} ({command.card.type})",
                f"Significado base: {command.card.base_meaning}",
            ]
        )
