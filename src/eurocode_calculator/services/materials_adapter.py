"""Adapter matériaux — eurocodepy principal, core comme fallback robuste."""

from eurocode_calculator.core.ec2_concrete import get_concrete_fck as core_get_concrete_fck
from eurocode_calculator.core.ec3_steel import get_steel_fyk as core_get_steel_fyk

_USE_EUROCODEPY: bool | None = None


def _eurocodepy_available() -> bool:
    """Vérifie si eurocodepy est installé et importable."""
    global _USE_EUROCODEPY
    if _USE_EUROCODEPY is None:
        try:
            import eurocodepy  # noqa: F401
            _USE_EUROCODEPY = True
        except ImportError:
            _USE_EUROCODEPY = False
    return _USE_EUROCODEPY


def get_concrete_fck(concrete_grade: str) -> float:
    """
    Retourne f_ck [MPa] pour une classe de béton.

    Utilise eurocodepy si disponible, sinon le catalogue interne `core`.
    """
    if _eurocodepy_available():
        try:
            import eurocodepy as ec

            concrete = ec.Concrete(concrete_grade)
            return float(concrete.fck)
        except Exception:
            pass
    return core_get_concrete_fck(concrete_grade)


def get_steel_fyk(steel_grade: str) -> float:
    """
    Retourne f_yk [MPa] pour une nuance d'acier.

    Utilise eurocodepy si disponible, sinon le catalogue interne `core`.
    """
    if _eurocodepy_available():
        try:
            import eurocodepy as ec

            steel = ec.Steel(steel_grade)
            return float(steel.fyk)
        except Exception:
            pass
    return core_get_steel_fyk(steel_grade)


def get_material_source() -> str:
    """Retourne la source matériaux active ('eurocodepy' ou 'core')."""
    return "eurocodepy" if _eurocodepy_available() else "core"
