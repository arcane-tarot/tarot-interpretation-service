from fastapi import APIRouter, Depends, HTTPException, status

from app.adapters.http import schemas
from app.application.commands import InterpretTarotCardCommand
from app.application.ports import TextGenerationError
from app.application.use_cases.interpret_tarot_card import (
    InterpretTarotCardUseCase,
)
from app.bootstrap import get_interpret_tarot_card_use_case
from app.domain.models import TarotCard

router = APIRouter(prefix="/api/tarot", tags=["tarot"])


@router.post(
    "/interpretations",
    response_model=schemas.InterpretTarotCardResponse,
    status_code=status.HTTP_200_OK,
)
def interpret_tarot_card(
    request: schemas.InterpretTarotCardRequest,
    use_case: InterpretTarotCardUseCase = Depends(get_interpret_tarot_card_use_case),
):
    command = InterpretTarotCardCommand(
        question=request.question,
        deck_type=request.deck_type,
        card=TarotCard(
            name=request.card.name,
            type=request.card.type,
            label=request.card.label,
            base_meaning=request.card.base_meaning,
        ),
    )

    try:
        result = use_case.execute(command)
    except TextGenerationError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error

    return schemas.InterpretTarotCardResponse(
        cardName=result.card_name,
        interpretation=result.interpretation,
    )
