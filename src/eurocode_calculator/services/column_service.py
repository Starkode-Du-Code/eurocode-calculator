"""Logique métier — flambement poteau acier EC3."""

from eurocode_calculator.core.ec3_steel import (
    calculate_buckling_reduction,
    calculate_buckling_resistance,
    calculate_slenderness,
    get_profile_properties,
    get_steel_fyk,
)
from eurocode_calculator.schemas.column import ColumnBucklingRequest, ColumnBucklingResponse


def verify_column_buckling(request: ColumnBucklingRequest) -> ColumnBucklingResponse:
    """
    Vérification au flambement d'un poteau métallique (EC3-1-1 §6.3).

    Utilise les propriétés de profilé du catalogue interne et la méthode analytique EC3.
    """
    fyk = get_steel_fyk(request.steel_grade)
    area_mm2, radius_of_gyration_mm = get_profile_properties(request.profile_name)

    lambda_bar = calculate_slenderness(
        length_mm=request.length_mm,
        radius_of_gyration_mm=radius_of_gyration_mm,
        fyk_mpa=fyk,
    )
    chi = calculate_buckling_reduction(lambda_bar, request.buckling_curve)
    buckling_resistance = calculate_buckling_resistance(
        area_mm2=area_mm2,
        fyk_mpa=fyk,
        lambda_bar=lambda_bar,
        curve=request.buckling_curve,
        gamma_m0=request.gamma_m0,
    )

    utilization = (
        request.axial_force_kn / buckling_resistance if buckling_resistance > 0 else float("inf")
    )
    verified = utilization <= 1.0

    if verified:
        message = f"Poteau OK — χ={chi:.3f}, taux {utilization:.1%}"
    else:
        message = (
            f"Flambement insuffisant — N_Ed={request.axial_force_kn:.0f} kN > "
            f"N_b,Rd={buckling_resistance:.0f} kN (taux {utilization:.1%})"
        )

    return ColumnBucklingResponse(
        verified=verified,
        steel_grade=request.steel_grade,
        profile_name=request.profile_name,
        fy_mpa=fyk,
        area_mm2=area_mm2,
        axial_force_ed_kn=request.axial_force_kn,
        buckling_resistance_kn=round(buckling_resistance, 1),
        slenderness=round(lambda_bar, 3),
        utilization_ratio=round(utilization, 4),
        message=message,
    )
