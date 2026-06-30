"""Logique métier — portance fondation EC7."""

from eurocode_calculator.schemas.foundation import (
    FoundationBearingRequest,
    FoundationBearingResponse,
)

# Résistances de portance caractéristiques typiques [kPa] — valeurs indicatives EC7
SOIL_BEARING_CAPACITY: dict[str, float] = {
    "dense_sand": 300.0,
    "medium_sand": 200.0,
    "loose_sand": 100.0,
    "stiff_clay": 150.0,
    "medium_clay": 75.0,
    "soft_clay": 30.0,
    "rock": 3000.0,
}


def verify_foundation_bearing(request: FoundationBearingRequest) -> FoundationBearingResponse:
    """
    Vérification de portance d'une semelle filante/isolée (EC7-1 §6.5).

    Méthode simplifiée : contrainte admissible = q_ult / γ_r.
    """
    q_ult = SOIL_BEARING_CAPACITY.get(request.soil_type.lower(), 150.0)
    bearing_resistance = q_ult / request.gamma_r

    area = request.foundation_width_m * request.foundation_length_m
    applied_pressure = request.vertical_load_kn / area

    utilization = applied_pressure / bearing_resistance if bearing_resistance > 0 else float("inf")
    verified = utilization <= 1.0

    if verified:
        message = f"Portance OK — σ_Ed={applied_pressure:.0f} kPa ≤ σ_Rd={bearing_resistance:.0f} kPa"
    else:
        message = (
            f"Portance insuffisante — σ_Ed={applied_pressure:.0f} kPa > "
            f"σ_Rd={bearing_resistance:.0f} kPa (augmenter la semelle ou améliorer le sol)"
        )

    return FoundationBearingResponse(
        verified=verified,
        soil_type=request.soil_type,
        bearing_resistance_kpa=round(bearing_resistance, 1),
        applied_pressure_kpa=round(applied_pressure, 1),
        foundation_area_m2=round(area, 3),
        utilization_ratio=round(utilization, 4),
        message=message,
    )
