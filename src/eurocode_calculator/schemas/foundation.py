"""Schémas Pydantic pour les endpoints fondation (EC7)."""

from pydantic import BaseModel, Field


class FoundationBearingRequest(BaseModel):
    """Données d'entrée pour la vérification de portance EC7."""

    soil_type: str = Field(
        default="dense_sand",
        description="Type de sol (catalogue eurocodepy ec7)",
        examples=["dense_sand", "medium_clay", "stiff_clay"],
    )
    foundation_width_m: float = Field(gt=0, description="Largeur de la semelle B [m]")
    foundation_length_m: float = Field(gt=0, description="Longueur de la semelle L [m]")
    embedment_depth_m: float = Field(
        default=0.0,
        ge=0,
        description="Profondeur d'encastrement D_f [m]",
    )
    vertical_load_kn: float = Field(gt=0, description="Charge verticale de calcul V_Ed [kN]")
    gamma_ground: float = Field(default=18.0, gt=0, description="Poids volumique du sol [kN/m³]")
    gamma_r: float = Field(default=1.25, gt=0, description="Coefficient partiel résistance γ_r")


class FoundationBearingResponse(BaseModel):
    """Résultat de la vérification de portance."""

    verified: bool = Field(description="True si σ_Ed ≤ σ_Rd")
    soil_type: str
    bearing_resistance_kpa: float = Field(description="Résistance de portance R_d [kPa]")
    applied_pressure_kpa: float = Field(description="Contrainte appliquée σ_Ed [kPa]")
    foundation_area_m2: float = Field(description="Surface de la semelle [m²]")
    utilization_ratio: float = Field(description="Taux d'utilisation σ_Ed / σ_Rd")
    message: str
