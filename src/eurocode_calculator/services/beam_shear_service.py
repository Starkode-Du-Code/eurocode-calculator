"""Vérification cisaillement EC2 — StructuralCodes capacity-based."""

from fastapi import HTTPException

from eurocode_calculator.schemas.beam import BeamVerifyShearRequest, BeamVerifyShearResponse
from eurocode_calculator.services.structuralcodes_setup import (
    STRUCTURALCODES_AVAILABLE,
    get_ec2_2004,
    parse_concrete_fck,
)


def verify_beam_shear(request: BeamVerifyShearRequest) -> BeamVerifyShearResponse:
    """
    Vérification cisaillement EN 1992-1-1 §6.2 via StructuralCodes.

    Sans étriers : V_Rdc. Avec étriers : min(V_Rds, V_Rd,max).
    """
    if not STRUCTURALCODES_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail=(
                "Vérification cisaillement capacity-based indisponible : "
                "StructuralCodes n'est pas installé. "
                "Installez l'extra [capacity] : pip install -e '.[capacity]'"
            ),
        )

    ec2 = get_ec2_2004()
    fck = parse_concrete_fck(request.concrete_grade)
    fcd = fck / request.gamma_c

    d_mm = request.height_mm - request.cover_mm - 10  # est. diamètre barre 10 mm
    z_mm = 0.9 * d_mm
    bw_mm = request.width_mm
    ac_mm2 = bw_mm * request.height_mm
    ned_n = request.axial_force_kn * 1000  # N (compression positive)

    v_rdc_n = ec2.VRdc(
        fck=fck,
        d=d_mm,
        Asl=request.longitudinal_steel_area_mm2,
        bw=bw_mm,
        NEd=ned_n,
        Ac=ac_mm2,
        fcd=fcd,
        gamma_c=request.gamma_c,
    )

    v_rds_n: float | None = None
    v_rdmax_n: float | None = None

    if request.stirrup_area_mm2 > 0 and request.stirrup_spacing_mm > 0:
        v_rds_n = ec2.VRds(
            Asw=request.stirrup_area_mm2,
            s=request.stirrup_spacing_mm,
            z=z_mm,
            theta=request.theta_deg,
            fyk=request.steel_fyk_mpa,
            gamma_s=request.gamma_s,
        )
        v_rdmax_n = ec2.VRdmax(
            bw=bw_mm,
            z=z_mm,
            fck=fck,
            theta=request.theta_deg,
            NEd=ned_n,
            Ac=ac_mm2,
            fcd=fcd,
        )
        v_rd_n = min(v_rdc_n + v_rds_n, v_rdmax_n)
    else:
        v_rd_n = v_rdc_n

    v_ed_n = request.shear_force_kn * 1000
    utilization = v_ed_n / v_rd_n if v_rd_n > 0 else float("inf")
    verified = utilization <= 1.0

    v_rdc_kn = v_rdc_n / 1000
    v_rd_kn = v_rd_n / 1000

    if verified:
        message = f"Cisaillement OK — V_Ed={request.shear_force_kn:.1f} kN ≤ V_Rd={v_rd_kn:.1f} kN"
    else:
        message = (
            f"Cisaillement insuffisant — V_Ed={request.shear_force_kn:.1f} kN > "
            f"V_Rd={v_rd_kn:.1f} kN (ajouter/reforcer étriers)"
        )

    return BeamVerifyShearResponse(
        verified=verified,
        concrete_grade=request.concrete_grade,
        shear_force_ed_kn=request.shear_force_kn,
        shear_resistance_kn=round(v_rd_kn, 2),
        v_rdc_kn=round(v_rdc_kn, 2),
        v_rds_kn=round(v_rds_n / 1000, 2) if v_rds_n else None,
        v_rdmax_kn=round(v_rdmax_n / 1000, 2) if v_rdmax_n else None,
        utilization_ratio=round(utilization, 4),
        message=message,
    )
