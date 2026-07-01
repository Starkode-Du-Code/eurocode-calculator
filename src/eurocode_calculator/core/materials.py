"""Propriétés matériaux Eurocodes (EC2 béton, EC3 acier)."""

# EN 1992-1-1 Table 3.1 — résistances caractéristiques f_ck [MPa]
CONCRETE_FCK_MPA: dict[str, float] = {
    "C12/15": 12.0,
    "C16/20": 16.0,
    "C20/25": 20.0,
    "C25/30": 25.0,
    "C30/37": 30.0,
    "C35/45": 35.0,
    "C40/50": 40.0,
    "C45/55": 45.0,
    "C50/60": 50.0,
    "C55/67": 55.0,
    "C60/75": 60.0,
    "C70/85": 70.0,
    "C80/95": 80.0,
    "C90/105": 90.0,
}

# EN 1993-1-1 Table 3.1 — limite d'élasticité f_yk [MPa]
STEEL_FYK_MPA: dict[str, float] = {
    "S235": 235.0,
    "S275": 275.0,
    "S355": 355.0,
    "S450": 450.0,
    "S460": 460.0,
}

# Module d'élasticité acier [MPa] — EN 1993-1-1 §3.2.6
E_STEEL_MPA: float = 210_000.0
