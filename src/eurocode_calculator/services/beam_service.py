"""Logique métier — vérification poutre béton EC2."""

from eurocode_calculator.schemas.beam import BeamVerifyULSRequest, BeamVerifyULSResponse
from eurocode_calculator.services.materials_adapter import get_concrete_fck


def verify_beam_uls(request: BeamVerifyULSRequest) -> BeamVerifyULSResponse:
    """
    Vérification ULS simplifiée en flexion simple d'une poutre rectangulaire en béton.

    Hypothèses :
    - Section rectangulaire pleine
    - Flexion simple sans armatures détaillées (estimation conservative)
    - Référence : EN 1992-1-1, flexion non armée (limite inférieure)

    Source matériaux : eurocodepy (principal) → core/fallback (interne)
    """
    fck = get_concrete_fck(request.concrete_grade)
    fcd = fck / request.gamma_c

    h_m = request.height_mm / 1000
    d_m = h_m - request.cover_mm / 1000 - 0.01  # enrobage + est. diamètre barre

    # Moment résistant simplifié (section rectangulaire, pivot A approximatif)
    b_mm = request.width_mm
    d_mm = d_m * 1000
    moment_rd_knm = 0.15 * fcd * b_mm * d_mm**2 / 1e6

    utilization = request.moment_knm / moment_rd_knm if moment_rd_knm > 0 else float("inf")
    verified = utilization <= 1.0

    if verified:
        message = f"Section OK — taux d'utilisation {utilization:.1%}"
    else:
        message = (
            f"Section insuffisante — M_Ed={request.moment_knm:.1f} kN·m > "
            f"M_Rd={moment_rd_knm:.1f} kN·m (taux {utilization:.1%})"
        )

    return BeamVerifyULSResponse(
        verified=verified,
        concrete_grade=request.concrete_grade,
        fck_mpa=fck,
        fcd_mpa=round(fcd, 2),
        moment_ed_knm=request.moment_knm,
        moment_rd_knm=round(moment_rd_knm, 2),
        utilization_ratio=round(utilization, 4),
        message=message,
    )
