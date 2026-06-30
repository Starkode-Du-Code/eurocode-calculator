"""Router — endpoints poutre EC2."""

from fastapi import APIRouter

from eurocode_calculator.schemas.beam import (
    BeamVerifyCapacityRequest,
    BeamVerifyCapacityResponse,
    BeamVerifyShearRequest,
    BeamVerifyShearResponse,
    BeamVerifyULSRequest,
    BeamVerifyULSResponse,
)
from eurocode_calculator.services.beam_capacity_service import verify_beam_capacity
from eurocode_calculator.services.beam_service import verify_beam_uls
from eurocode_calculator.services.beam_shear_service import verify_beam_shear

router = APIRouter(prefix="/beam", tags=["Poutre — EC2"])


@router.post(
    "/verify-uls",
    response_model=BeamVerifyULSResponse,
    summary="Vérification ULS poutre béton (simplifiée)",
    description="Pré-dimensionnement rapide en flexion simple (EN 1992-1-1, eurocodepy).",
)
def post_verify_uls(request: BeamVerifyULSRequest) -> BeamVerifyULSResponse:
    return verify_beam_uls(request)


@router.post(
    "/verify-shear",
    response_model=BeamVerifyShearResponse,
    summary="Vérification cisaillement EC2",
    description="Vérification effort tranchant via StructuralCodes (EN 1992-1-1 §6.2).",
)
def post_verify_shear(request: BeamVerifyShearRequest) -> BeamVerifyShearResponse:
    return verify_beam_shear(request)


@router.post(
    "/verify-uls-capacity",
    response_model=BeamVerifyCapacityResponse,
    summary="Vérification flexion capacity-based",
    description=(
        "Vérification ULS complète avec armatures via StructuralCodes BeamSection "
        "(moment-courbure, capacity-based design)."
    ),
)
def post_verify_uls_capacity(request: BeamVerifyCapacityRequest) -> BeamVerifyCapacityResponse:
    return verify_beam_capacity(request)
