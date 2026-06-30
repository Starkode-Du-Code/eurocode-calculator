"""Initialisation partagée StructuralCodes (EC2 capacity-based design)."""

from structuralcodes import set_design_code
from structuralcodes.codes import ec2_2004
from structuralcodes.geometry import RectangularGeometry, add_reinforcement
from structuralcodes.materials.concrete import ConcreteEC2_2004
from structuralcodes.materials.reinforcement import ReinforcementEC2_2004
from structuralcodes.sections import BeamSection

# EC2 (2004) — norme supportée par StructuralCodes
_DESIGN_CODE = "ec2_2004"
_initialized = False


def ensure_ec2_design_code() -> None:
    """Configure le code de calcul EC2 une seule fois par processus."""
    global _initialized
    if not _initialized:
        set_design_code(_DESIGN_CODE)
        _initialized = True


def parse_concrete_fck(concrete_grade: str) -> float:
    """Extrait fck depuis une classe 'C30/37' → 30.0."""
    return float(concrete_grade.upper().replace("C", "").split("/")[0])


def create_concrete_material(fck: float) -> ConcreteEC2_2004:
    """Crée un matériau béton EC2 via StructuralCodes."""
    ensure_ec2_design_code()
    return ConcreteEC2_2004(fck=fck)


def create_reinforcement_material(fyk: float = 500.0) -> ReinforcementEC2_2004:
    """Crée un matériau acier B500B (valeurs EC2 typiques)."""
    ensure_ec2_design_code()
    return ReinforcementEC2_2004(
        fyk=fyk,
        Es=200_000.0,
        ftk=550.0,
        epsuk=0.05,
    )


def build_rectangular_beam_section(
    width_mm: float,
    height_mm: float,
    concrete_grade: str,
    bottom_bar_diameter_mm: float,
    bottom_bar_count: int,
    cover_mm: float,
    steel_fyk: float = 500.0,
) -> BeamSection:
    """
    Construit une section poutre rectangulaire avec armatures inférieures.

    Armatures réparties uniformément sur la largeur utile.
    """
    fck = parse_concrete_fck(concrete_grade)
    concrete = create_concrete_material(fck)
    steel = create_reinforcement_material(steel_fyk)

    geom = RectangularGeometry(width=width_mm, height=height_mm, material=concrete)

    if bottom_bar_count > 0 and bottom_bar_diameter_mm > 0:
        y = cover_mm + bottom_bar_diameter_mm / 2
        usable_width = width_mm - 2 * cover_mm - bottom_bar_diameter_mm
        spacing = usable_width / max(bottom_bar_count - 1, 1)
        for i in range(bottom_bar_count):
            x = cover_mm + bottom_bar_diameter_mm / 2 + i * spacing
            geom = add_reinforcement(
                geom,
                coords=(x, y),
                diameter=bottom_bar_diameter_mm,
                material=steel,
            )

    return BeamSection(geometry=geom)


def get_ec2_2004():
    """Retourne le module d'équations EC2 après initialisation."""
    ensure_ec2_design_code()
    return ec2_2004
