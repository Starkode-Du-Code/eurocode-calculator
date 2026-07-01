"""Calculs béton armé EC2 — implémentation propre sans eurocodepy."""

from dataclasses import dataclass

from eurocode_calculator.core.materials import CONCRETE_FCK_MPA


@dataclass(frozen=True)
class ConcreteGrade:
    """Classe de béton EC2 avec sa résistance caractéristique."""

    name: str
    fck_mpa: float


def parse_concrete_fck(concrete_grade: str) -> float:
    """Extrait fck depuis une classe 'C30/37' → 30.0."""
    return float(concrete_grade.upper().replace("C", "").split("/")[0])


def get_concrete_fck(concrete_grade: str) -> float:
    """Retourne f_ck [MPa] pour une classe de béton donnée."""
    grade = concrete_grade.upper()
    if grade in CONCRETE_FCK_MPA:
        return CONCRETE_FCK_MPA[grade]
    # Fallback : parsing du libellé (ex: C30/37 → 30)
    return parse_concrete_fck(grade)


def calculate_concrete_fcd(fck_mpa: float, gamma_c: float = 1.5) -> float:
    """Résistance de calcul du béton en compression f_cd [MPa]."""
    return fck_mpa / gamma_c


def calculate_simplified_moment_resistance(
    width_mm: float,
    height_mm: float,
    cover_mm: float,
    fck_mpa: float,
    gamma_c: float = 1.5,
    bar_diameter_mm: float = 20.0,
) -> tuple[float, float, float]:
    """
    Moment résistant simplifié d'une section rectangulaire en béton armé [kN·m].

    Hypothèses conservatrices (pré-dimensionnement) :
    - Hauteur utile d = h - cover - Øbarre/2
    - Pivot A approximatif : M_Rd ≈ 0.15 · f_cd · b · d²

    Retourne (fcd_mpa, d_mm, moment_rd_knm).
    """
    fcd = calculate_concrete_fcd(fck_mpa, gamma_c)
    d_mm = height_mm - cover_mm - bar_diameter_mm / 2
    if d_mm <= 0 or width_mm <= 0:
        return fcd, d_mm, 0.0

    moment_rd_knm = 0.15 * fcd * width_mm * d_mm**2 / 1e6
    return fcd, d_mm, moment_rd_knm


def verify_uls_moment(
    width_mm: float,
    height_mm: float,
    cover_mm: float,
    fck_mpa: float,
    moment_ed_knm: float,
    gamma_c: float = 1.5,
    bar_diameter_mm: float = 20.0,
) -> dict:
    """Vérification ULS moment EC2 simplifiée."""
    fcd, d_mm, moment_rd_knm = calculate_simplified_moment_resistance(
        width_mm=width_mm,
        height_mm=height_mm,
        cover_mm=cover_mm,
        fck_mpa=fck_mpa,
        gamma_c=gamma_c,
        bar_diameter_mm=bar_diameter_mm,
    )

    ratio = moment_ed_knm / moment_rd_knm if moment_rd_knm > 0 else float("inf")
    status = "OK" if ratio <= 1.0 else "FAIL"

    return {
        "fcd_mpa": round(fcd, 2),
        "d_mm": round(d_mm, 2),
        "moment_rd_knm": round(moment_rd_knm, 2),
        "moment_ed_knm": moment_ed_knm,
        "ratio": round(ratio, 4),
        "status": status,
        "code": "EC2-1-1 §6.1 (simplified)",
    }
