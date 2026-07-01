"""Router — génération de rapports PDF."""

from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from eurocode_calculator.services.pdf_generator import generate_report

router = APIRouter(prefix="/report", tags=["Rapport PDF"])


class Calculation(BaseModel):
    """Calcul intermédiaire affiché dans le rapport."""

    label: str = Field(description="Nom du calcul")
    formula: str = Field(description="Formule littérale")
    result: str = Field(description="Valeur numérique obtenue")
    unit: str = Field(default="", description="Unité")


class Check(BaseModel):
    """Vérification structurale avec ratio et statut."""

    name: str = Field(description="Nom de la vérification")
    formula: str = Field(description="Formule de vérification")
    result: str = Field(description="Comparaison littérale")
    ratio: str = Field(description="Ratio d'utilisation")
    status: str = Field(description="OK, WARNING ou FAIL")


class Diagram(BaseModel):
    """Diagramme de moment fléchissant à générer."""

    L: float = Field(description="Portée [m]")
    q: float = Field(description="Charge uniforme [kN/m]")
    M_Ed: float = Field(description="Moment de calcul [kN·m]")
    caption: str = Field(default="Diagramme de moment fléchissant", description="Légende")


class ReportElement(BaseModel):
    """Élément structuré inclus dans un rapport PDF."""

    type: str = Field(description="Type d'élément (Poutre, Poteau, Semelle)")
    name: str = Field(description="Nom ou référence de l'élément")
    inputs: dict[str, str] = Field(description="Paramètres d'entrée")
    status: str = Field(default="ok", description="ok, warning ou fail")
    result: str = Field(default="", description="Résultat textuel")
    ratio: str = Field(default="", description="Ratio d'utilisation")
    code: str = Field(default="", description="Clause norme appliquée")
    message: str = Field(default="", description="Message détaillé")
    calculations: list[Calculation] = Field(default_factory=list, description="Calculs intermédiaires")
    checks: list[Check] = Field(default_factory=list, description="Vérifications")
    diagrams: list[Diagram] = Field(default_factory=list, description="Diagrammes")


class ReportRequest(BaseModel):
    """Données d'entrée pour la génération d'un rapport PDF."""

    project_name: str = Field(default="Projet", description="Nom du projet")
    elements: list[ReportElement] = Field(description="Liste des éléments calculés")


@router.post(
    "/generate",
    summary="Générer un rapport PDF personnalisé",
    description="Génère un PDF professionnel à partir des résultats de calculs structurels.",
)
async def generate_pdf(request: ReportRequest):
    """Génère un rapport PDF de vérification Eurocodes personnalisable."""
    elements = [el.model_dump() for el in request.elements]
    pdf_path = generate_report(
        project_name=request.project_name,
        elements=elements,
    )
    safe_name = request.project_name.lower().replace(" ", "_")
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"rapport_{safe_name}.pdf",
    )


@router.post(
    "/demo",
    summary="Générer un rapport PDF de démonstration",
    description="Retourne un rapport PDF complet avec un cas réel de poutre béton armé.",
)
async def generate_demo_pdf():
    """Génère un rapport PDF de démonstration avec un cas réel complet."""
    project_data = {
        "project_name": "Vérification Poutre RDC — Bâtiment Bureau",
        "elements": [
            {
                "type": "Poutre béton armé",
                "name": "P1-RDC (Portée 6,00 m)",
                "status": "ok",
                "inputs": {
                    "Portée L": "6,00 m",
                    "Section b × h": "300 × 500 mm",
                    "Enrobage c": "30 mm",
                    "Béton": "C25/30 (fck = 25 MPa)",
                    "Acier": "B500B (fyk = 500 MPa)",
                    "Charge permanente gk": "25 kN/m",
                    "Charge d'exploitation qk": "15 kN/m",
                },
                "calculations": [
                    {
                        "label": "Charge ELU",
                        "formula": "qEd = 1,35·gk + 1,50·qk",
                        "result": "56,25",
                        "unit": "kN/m",
                    },
                    {
                        "label": "Moment ELU",
                        "formula": "MEd = qEd·L²/8",
                        "result": "253,1",
                        "unit": "kN·m",
                    },
                    {
                        "label": "Hauteur utile",
                        "formula": "d = h - c - Ø/2",
                        "result": "452",
                        "unit": "mm",
                    },
                    {
                        "label": "Moment résistant",
                        "formula": "MRd = 0,167·b·d²·fcd",
                        "result": "312,4",
                        "unit": "kN·m",
                    },
                ],
                "checks": [
                    {
                        "name": "Flexion ULS",
                        "formula": "MEd ≤ MRd",
                        "result": "253,1 ≤ 312,4",
                        "ratio": "0.81",
                        "status": "OK",
                    },
                    {
                        "name": "Effort tranchant",
                        "formula": "VEd ≤ VRd,c",
                        "result": "168,8 ≤ 245,3",
                        "ratio": "0.69",
                        "status": "OK",
                    },
                    {
                        "name": "Fissuration SLS",
                        "formula": "wk ≤ 0,3 mm",
                        "result": "0,18 ≤ 0,30",
                        "ratio": "0.60",
                        "status": "OK",
                    },
                    {
                        "name": "Armature min",
                        "formula": "As,min = 0,26·(fctm/fyk)·b·d",
                        "result": "As = 4,52 cm² ≥ 2,81 cm²",
                        "ratio": "0.62",
                        "status": "OK",
                    },
                ],
                "diagrams": [
                    {
                        "L": 6.0,
                        "q": 56.25,
                        "M_Ed": 253.1,
                        "caption": "Diagramme de moment fléchissant sous charge ELU",
                    },
                ],
            },
        ],
    }

    pdf_path = generate_report(
        project_name=project_data["project_name"],
        elements=project_data["elements"],
    )
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="Rapport_Verification_Poutre_RDC.pdf",
    )
