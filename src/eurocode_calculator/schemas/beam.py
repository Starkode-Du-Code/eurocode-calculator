"""Schémas Pydantic pour les endpoints poutre (EC2)."""

from pydantic import BaseModel, Field


class BeamVerifyULSRequest(BaseModel):
    """Données d'entrée pour la vérification ULS d'une poutre en béton armé."""

    concrete_grade: str = Field(
        default="C30/37",
        description="Classe de béton selon EN 1992-1-1 (ex: C25/30, C30/37)",
        examples=["C25/30", "C30/37", "C40/50"],
    )
    width_mm: float = Field(gt=0, description="Largeur de la section [mm]", examples=[300])
    height_mm: float = Field(gt=0, description="Hauteur totale de la section [mm]", examples=[500])
    cover_mm: float = Field(default=30, ge=0, description="Enrobage nominal [mm]")
    moment_knm: float = Field(description="Moment de calcul M_Ed [kN·m]")
    gamma_c: float = Field(default=1.5, gt=0, description="Coefficient partiel béton γ_c")


class BeamVerifyULSResponse(BaseModel):
    """Résultat de la vérification ULS."""

    verified: bool = Field(description="True si la section satisfait M_Ed ≤ M_Rd")
    concrete_grade: str
    fck_mpa: float = Field(description="Résistance caractéristique f_ck [MPa]")
    fcd_mpa: float = Field(description="Résistance de calcul f_cd [MPa]")
    moment_ed_knm: float = Field(description="Moment de calcul M_Ed [kN·m]")
    moment_rd_knm: float = Field(description="Moment résistant M_Rd [kN·m]")
    utilization_ratio: float = Field(description="Taux d'utilisation M_Ed / M_Rd")
    message: str
    calculation_method: str = Field(
        default="simplified",
        description="Méthode : simplified (eurocodepy) ou capacity-based (StructuralCodes)",
    )


class BeamVerifyShearRequest(BaseModel):
    """Données d'entrée pour la vérification cisaillement EC2 §6.2."""

    concrete_grade: str = Field(default="C30/37", examples=["C25/30", "C30/37"])
    width_mm: float = Field(gt=0, description="Largeur utile b_w [mm]")
    height_mm: float = Field(gt=0, description="Hauteur totale h [mm]")
    cover_mm: float = Field(default=30, ge=0, description="Enrobage nominal [mm]")
    shear_force_kn: float = Field(gt=0, description="Effort tranchant de calcul V_Ed [kN]")
    axial_force_kn: float = Field(
        default=0.0,
        description="Effort normal N_Ed [kN] (positif = compression)",
    )
    longitudinal_steel_area_mm2: float = Field(
        default=0.0,
        ge=0,
        description="Aire acier longitudinal tendu A_sl [mm²]",
    )
    stirrup_area_mm2: float = Field(
        default=0.0,
        ge=0,
        description="A_sw — aire brins étriers sur une jambe [mm²]",
    )
    stirrup_spacing_mm: float = Field(default=0.0, ge=0, description="Entraxe étriers s [mm]")
    steel_fyk_mpa: float = Field(default=500.0, gt=0, description="f_yk acier [MPa]")
    gamma_c: float = Field(default=1.5, gt=0)
    gamma_s: float = Field(default=1.15, gt=0)
    theta_deg: float = Field(default=45.0, gt=0, le=90, description="Angle bielle compression [°]")


class BeamVerifyShearResponse(BaseModel):
    """Résultat vérification cisaillement — StructuralCodes EC2."""

    verified: bool
    concrete_grade: str
    shear_force_ed_kn: float
    shear_resistance_kn: float = Field(description="V_Rd [kN] (béton + éventuels étriers)")
    v_rdc_kn: float = Field(description="Contribution béton V_Rdc [kN]")
    v_rds_kn: float | None = Field(default=None, description="Contribution étriers V_Rds [kN]")
    v_rdmax_kn: float | None = Field(default=None, description="Plafond bielle V_Rd,max [kN]")
    utilization_ratio: float
    calculation_method: str = "capacity-based-structuralcodes"
    message: str


class BeamVerifyCapacityRequest(BaseModel):
    """Vérification flexion ULS capacity-based avec armatures (StructuralCodes)."""

    concrete_grade: str = Field(default="C30/37")
    width_mm: float = Field(gt=0)
    height_mm: float = Field(gt=0)
    cover_mm: float = Field(default=30, ge=0)
    moment_knm: float = Field(description="Moment de calcul M_Ed [kN·m]")
    bottom_bar_diameter_mm: float = Field(
        default=16,
        gt=0,
        description="Diamètre barres inférieures [mm]",
    )
    bottom_bar_count: int = Field(default=3, ge=1, description="Nombre de barres inférieures")
    steel_fyk_mpa: float = Field(default=500.0, gt=0)


class BeamVerifyCapacityResponse(BaseModel):
    """Résultat flexion capacity-based — StructuralCodes BeamSection."""

    verified: bool
    concrete_grade: str
    moment_ed_knm: float
    moment_rd_knm: float = Field(description="M_Rd capacity-based [kN·m]")
    utilization_ratio: float
    reinforcement_area_mm2: float
    calculation_method: str = "capacity-based-structuralcodes"
    message: str
