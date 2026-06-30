"""Router — endpoints fondation EC7."""

from fastapi import APIRouter

from eurocode_calculator.schemas.foundation import (
    FoundationBearingRequest,
    FoundationBearingResponse,
)
from eurocode_calculator.services.foundation_service import verify_foundation_bearing

router = APIRouter(prefix="/foundation", tags=["Fondation — EC7"])


@router.post(
    "/bearing",
    response_model=FoundationBearingResponse,
    summary="Vérification portance fondation",
    description="Vérifie la portance d'une semelle superficielle selon EN 1997-1.",
)
def post_bearing(request: FoundationBearingRequest) -> FoundationBearingResponse:
    return verify_foundation_bearing(request)
