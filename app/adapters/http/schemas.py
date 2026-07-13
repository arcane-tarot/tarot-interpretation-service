from pydantic import BaseModel, ConfigDict, Field


class ApiSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TarotCardRequest(ApiSchema):
    name: str = Field(min_length=1, max_length=100)
    type: str = Field(min_length=1, max_length=30)
    label: str = Field(min_length=1, max_length=60)
    base_meaning: str = Field(
        alias="baseMeaning",
        min_length=1,
        max_length=600,
    )


class InterpretTarotCardRequest(ApiSchema):
    question: str = Field(min_length=1, max_length=800)
    deck_type: str = Field(alias="deckType", min_length=1, max_length=30)
    card: TarotCardRequest


class InterpretTarotCardResponse(ApiSchema):
    card_name: str = Field(alias="cardName")
    interpretation: str
