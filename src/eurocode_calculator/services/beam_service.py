"""Logique métier — vérification poutre béton EC2."""

from eurocode_calculator.core.ec2_concrete import (
    calculate_simplified_moment_resistance,
    get_concrete_fck,
)
from eurocode_calculator.schemas.beam import BeamVerifyULSRequest, BeamVerifyULSResponse


def verify_beam_uls(request: BeamVerifyULSRequest) -> BeamVerifyULSResponse:
    """
    Vérification ULS simplifiée en flexion simple d'une poutre rectangulaire en béton.

    Hypothèses :
    - Section rectangulaire pleine
    - Flexion simple sans armatures détaillées (estimation conservative)
    - Référence : EN 1992-1-1, flexion non armée (limite inférieure)
    """
    fck = get_concrete_fck(request.concrete_grade)

    fcd, _d_mm, moment_rd_knm = calculate_simplified_moment_resistance(
        width_mm=request.width_mm,
        height_mm=request.height_mm,
        cover_mm=request.cover_mm,
        fck_mpa=fck,
        gamma_c=request.gamma_c,
        bar_diameter_mm=20.0,
    )

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
