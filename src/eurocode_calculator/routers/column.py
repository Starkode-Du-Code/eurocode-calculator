"""Router — endpoints poteau EC3."""

from fastapi import APIRouter

from eurocode_calculator.schemas.column import ColumnBucklingRequest, ColumnBucklingResponse
from eurocode_calculator.services.column_service import verify_column_buckling

router = APIRouter(prefix="/column", tags=["Poteau — EC3"])


@router.post(
    "/buckling",
    response_model=ColumnBucklingResponse,
    summary="Vérification flambement poteau acier",
    description="Vérifie un poteau métallique au flambement selon EN 1993-1-1 §6.3.",
)
def post_buckling(request: ColumnBucklingRequest) -> ColumnBucklingResponse:
    return verify_column_buckling(request)
