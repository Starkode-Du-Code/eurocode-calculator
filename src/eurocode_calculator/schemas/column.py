"""Schémas Pydantic pour les endpoints poteau (EC3)."""

from pydantic import BaseModel, Field


class ColumnBucklingRequest(BaseModel):
    """Données d'entrée pour la vérification au flambement EC3."""

    steel_grade: str = Field(
        default="S355",
        description="Nuance d'acier selon EN 1993-1-1",
        examples=["S235", "S355", "S450"],
    )
    profile_name: str = Field(
        default="HEA200",
        description="Profilé métallique (catalogue eurocodepy)",
        examples=["HEA200", "IPE300", "HEB260"],
    )
    length_mm: float = Field(gt=0, description="Longueur de flambement L [mm]")
    axial_force_kn: float = Field(gt=0, description="Effort normal de calcul N_Ed [kN]")
    buckling_curve: str = Field(
        default="b",
        description="Courbe de flambement (a, b, c, d)",
        examples=["a", "b", "c", "d"],
    )
    gamma_m0: float = Field(default=1.0, gt=0, description="Coefficient partiel γ_M0")


class ColumnBucklingResponse(BaseModel):
    """Résultat de la vérification au flambement."""

    verified: bool = Field(description="True si N_Ed ≤ N_b,Rd")
    steel_grade: str
    profile_name: str
    fy_mpa: float = Field(description="Limite d'élasticité f_y [MPa]")
    area_mm2: float = Field(description="Aire de la section A [mm²]")
    axial_force_ed_kn: float = Field(description="Effort normal N_Ed [kN]")
    buckling_resistance_kn: float = Field(description="Résistance au flambement N_b,Rd [kN]")
    slenderness: float = Field(description="Élancement non adimensionné λ̄")
    utilization_ratio: float = Field(description="Taux d'utilisation N_Ed / N_b,Rd")
    message: str
