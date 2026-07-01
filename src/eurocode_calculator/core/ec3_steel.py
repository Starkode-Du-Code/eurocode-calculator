"""Calculs acier et flambement EC3 — implémentation propre sans eurocodepy."""

import math

from eurocode_calculator.core.materials import E_STEEL_MPA, STEEL_FYK_MPA

# Catalogue simplifié de profilés laminés : (aire A [mm²], rayon de giration i_y [mm])
# Valeurs indicatives issues de catalogues de profilés pour les sections courantes.
STEEL_PROFILE_CATALOG: dict[str, tuple[float, float]] = {
    "HEA100": (2120.0, 41.6),
    "HEA120": (2530.0, 49.8),
    "HEA140": (3140.0, 58.4),
    "HEA160": (3880.0, 67.2),
    "HEA180": (4530.0, 75.9),
    "HEA200": (5380.0, 85.3),
    "HEA220": (6430.0, 95.1),
    "HEA240": (7680.0, 104.5),
    "HEA260": (8680.0, 111.0),
    "HEA300": (11250.0, 127.5),
    "HEA400": (15880.0, 159.0),
    "HEB100": (2600.0, 41.2),
    "HEB120": (3400.0, 49.7),
    "HEB140": (4290.0, 58.0),
    "HEB160": (5430.0, 66.6),
    "HEB180": (6520.0, 75.1),
    "HEB200": (7810.0, 84.6),
    "HEB220": (9100.0, 93.9),
    "HEB240": (10600.0, 103.1),
    "HEB260": (11840.0, 109.7),
    "HEB300": (14910.0, 125.8),
    "HEB400": (19780.0, 155.6),
    "IPE100": (1030.0, 41.1),
    "IPE120": (1320.0, 49.6),
    "IPE140": (1640.0, 58.2),
    "IPE160": (2010.0, 67.0),
    "IPE180": (2390.0, 75.7),
    "IPE200": (2850.0, 84.6),
    "IPE220": (3340.0, 93.9),
    "IPE240": (3910.0, 103.3),
    "IPE270": (4590.0, 115.1),
    "IPE300": (5380.0, 121.0),
    "IPE330": (6280.0, 135.0),
    "IPE360": (7270.0, 147.0),
    "IPE400": (8450.0, 159.0),
    "IPE450": (9880.0, 173.0),
    "IPE500": (11550.0, 185.0),
}

# Courbes de flambement EN 1993-1-1 §6.3.2.2 — facteur d'imperfection α
BUCKLING_CURVE_ALPHA: dict[str, float] = {
    "a0": 0.13,
    "a": 0.21,
    "b": 0.34,
    "c": 0.49,
    "d": 0.76,
}


class SteelGrade:
    """Nuance d'acier EC3."""

    def __init__(self, name: str, fyk_mpa: float):
        self.name = name
        self.fyk_mpa = fyk_mpa


def get_steel_fyk(steel_grade: str) -> float:
    """Retourne f_yk [MPa] pour une nuance d'acier donnée."""
    grade = steel_grade.upper()
    return STEEL_FYK_MPA.get(grade, 355.0)


def get_profile_properties(profile_name: str) -> tuple[float, float]:
    """Retourne (aire [mm²], rayon de giration i_y [mm]) pour un profilé."""
    return STEEL_PROFILE_CATALOG.get(profile_name.upper(), (5380.0, 85.3))


def calculate_slenderness(
    length_mm: float,
    radius_of_gyration_mm: float,
    fyk_mpa: float,
    e_modulus_mpa: float = E_STEEL_MPA,
) -> float:
    """Élancement non adimensionnel λ̄ selon EC3-1-1 §6.3.1.2."""
    slenderness = (length_mm / 1000) / (radius_of_gyration_mm / 1000)
    lambda_1 = math.pi * math.sqrt(e_modulus_mpa / fyk_mpa)
    return slenderness / lambda_1


def calculate_buckling_reduction(lambda_bar: float, curve: str = "b") -> float:
    """Facteur de réduction au flambement χ selon EC3-1-1 §6.3.2.2."""
    alpha = BUCKLING_CURVE_ALPHA.get(curve.lower(), 0.34)

    phi = 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2)
    chi = 1.0 / (phi + math.sqrt(max(phi**2 - lambda_bar**2, 0)))
    return min(chi, 1.0)


def calculate_buckling_resistance(
    area_mm2: float,
    fyk_mpa: float,
    lambda_bar: float,
    curve: str = "b",
    gamma_m0: float = 1.0,
) -> float:
    """Résistance au flambement N_b,Rd [kN]."""
    chi = calculate_buckling_reduction(lambda_bar, curve)
    n_pl_rd = area_mm2 * fyk_mpa / (gamma_m0 * 1000)
    return chi * n_pl_rd


def verify_column_buckling(
    steel_grade: str,
    profile_name: str,
    length_mm: float,
    axial_force_kn: float,
    buckling_curve: str = "b",
    gamma_m0: float = 1.0,
) -> dict:
    """Vérification complète au flambement EC3-1-1 §6.3."""
    fyk = get_steel_fyk(steel_grade)
    area_mm2, radius_of_gyration_mm = get_profile_properties(profile_name)

    lambda_bar = calculate_slenderness(length_mm, radius_of_gyration_mm, fyk)
    chi = calculate_buckling_reduction(lambda_bar, buckling_curve)
    buckling_resistance_kn = calculate_buckling_resistance(
        area_mm2=area_mm2,
        fyk_mpa=fyk,
        lambda_bar=lambda_bar,
        curve=buckling_curve,
        gamma_m0=gamma_m0,
    )

    utilization = axial_force_kn / buckling_resistance_kn if buckling_resistance_kn > 0 else float("inf")
    status = "OK" if utilization <= 1.0 else "FAIL"

    return {
        "fyk_mpa": fyk,
        "area_mm2": area_mm2,
        "radius_of_gyration_mm": radius_of_gyration_mm,
        "lambda_bar": round(lambda_bar, 3),
        "chi": round(chi, 3),
        "buckling_resistance_kn": round(buckling_resistance_kn, 1),
        "axial_force_ed_kn": axial_force_kn,
        "utilization_ratio": round(utilization, 4),
        "status": status,
        "code": "EC3-1-1 §6.3",
    }
