from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.application.ports import TextGenerator
from app.bootstrap import get_text_generator

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/live")
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/startup")
def startup() -> dict[str, str]:
    return {"status": "started"}


@router.get("/ready")
def readiness(
    text_generator: TextGenerator = Depends(get_text_generator),
):
    if not text_generator.is_ready():
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {"openai_api_key": "missing"},
            },
        )

    return {
        "status": "ready",
        "checks": {"openai_api_key": "configured"},
    }
