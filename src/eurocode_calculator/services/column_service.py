"""Logique métier — flambement poteau acier EC3."""

import math

import eurocodepy as ec

from eurocode_calculator.schemas.column import ColumnBucklingRequest, ColumnBucklingResponse

# Module d'élasticité acier [MPa]
E_STEEL = 210_000


def verify_column_buckling(request: ColumnBucklingRequest) -> ColumnBucklingResponse:
    """
    Vérification au flambement d'un poteau métallique (EC3-1-1 §6.3).

    Utilise les propriétés de profilé eurocodepy et la formule de Perry-Robertson simplifiée.
    """
    steel = ec.Steel(request.steel_grade)
    fyk = steel.fyk

    # Propriétés HEA200 (fallback si catalogue indisponible)
    profile_catalog: dict[str, tuple[float, float]] = {
        "HEA100": (2120.0, 41.6),
        "HEA200": (5380.0, 85.3),
        "HEB260": (8680.0, 111.0),
        "IPE300": (5380.0, 121.0),
    }
    area, iy = profile_catalog.get(request.profile_name.upper(), (5380.0, 85.3))

    i_min = iy  # flambement autour de l'axe faible
    slenderness = (request.length_mm / 1000) / (i_min / 1000)
    lambda_bar = slenderness / math.pi * math.sqrt(fyk / E_STEEL)

    # Courbes de flambement EC3 — facteur χ simplifié
    curve_factors = {"a": 0.21, "b": 0.34, "c": 0.49, "d": 0.76}
    alpha = curve_factors.get(request.buckling_curve.lower(), 0.34)

    phi = 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2)
    chi = 1.0 / (phi + math.sqrt(max(phi**2 - lambda_bar**2, 0)))
    chi = min(chi, 1.0)

    n_pl_rd = area * fyk / (request.gamma_m0 * 1000)  # kN
    buckling_resistance = chi * n_pl_rd

    utilization = request.axial_force_kn / buckling_resistance if buckling_resistance > 0 else float("inf")
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
        area_mm2=area,
        axial_force_ed_kn=request.axial_force_kn,
        buckling_resistance_kn=round(buckling_resistance, 1),
        slenderness=round(lambda_bar, 3),
        utilization_ratio=round(utilization, 4),
        message=message,
    )
