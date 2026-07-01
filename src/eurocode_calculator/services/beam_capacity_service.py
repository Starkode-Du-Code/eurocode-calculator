"""Vérification flexion capacity-based — StructuralCodes BeamSection."""

import math

from fastapi import HTTPException

from eurocode_calculator.schemas.beam import BeamVerifyCapacityRequest, BeamVerifyCapacityResponse
from eurocode_calculator.services.structuralcodes_setup import (
    STRUCTURALCODES_AVAILABLE,
    build_rectangular_beam_section,
)


def verify_beam_capacity(request: BeamVerifyCapacityRequest) -> BeamVerifyCapacityResponse:
    """
    Vérification ULS flexion avec armatures via StructuralCodes.

    Utilise BeamSection.calculate_bending_strength() — capacity-based design complet.
    Référence : EN 1992-1-1 via structuralcodes.codes.ec2_2004
    """
    if not STRUCTURALCODES_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail=(
                "Capacity-based design indisponible : StructuralCodes n'est pas installé. "
                "Installez l'extra [capacity] : pip install -e '.[capacity]'"
            ),
        )

    section = build_rectangular_beam_section(
        width_mm=request.width_mm,
        height_mm=request.height_mm,
        concrete_grade=request.concrete_grade,
        bottom_bar_diameter_mm=request.bottom_bar_diameter_mm,
        bottom_bar_count=request.bottom_bar_count,
        cover_mm=request.cover_mm,
        steel_fyk=request.steel_fyk_mpa,
    )

    result = section.section_calculator.calculate_bending_strength()
    # m_y en N·mm (convention SC : négatif en flexion positive)
    moment_rd_knm = abs(result.m_y) / 1e6

    bar_area = math.pi * (request.bottom_bar_diameter_mm / 2) ** 2
    reinforcement_area = bar_area * request.bottom_bar_count

    utilization = request.moment_knm / moment_rd_knm if moment_rd_knm > 0 else float("inf")
    verified = utilization <= 1.0

    if verified:
        bars = f"{request.bottom_bar_count}Ø{request.bottom_bar_diameter_mm:.0f}"
        message = (
            f"Flexion capacity-based OK — M_Ed={request.moment_knm:.1f} kN·m ≤ "
            f"M_Rd={moment_rd_knm:.1f} kN·m ({bars})"
        )
    else:
        message = (
            f"Flexion insuffisante — M_Ed={request.moment_knm:.1f} kN·m > "
            f"M_Rd={moment_rd_knm:.1f} kN·m (augmenter armatures)"
        )

    return BeamVerifyCapacityResponse(
        verified=verified,
        concrete_grade=request.concrete_grade,
        moment_ed_knm=request.moment_knm,
        moment_rd_knm=round(moment_rd_knm, 2),
        utilization_ratio=round(utilization, 4),
        reinforcement_area_mm2=round(reinforcement_area, 1),
        message=message,
    )
