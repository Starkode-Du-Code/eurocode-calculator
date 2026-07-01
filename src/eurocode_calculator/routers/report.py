"""Router — génération de rapports PDF."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from eurocode_calculator.services.pdf_generator import generate_report

router = APIRouter(prefix="/report", tags=["Rapport PDF"])


class ReportElement(BaseModel):
    """Élément structuré inclus dans un rapport PDF."""

    type: str = Field(description="Type d'élément (Poutre, Poteau, Semelle)")
    name: str = Field(description="Nom ou référence de l'élément")
    inputs: dict[str, str] = Field(description="Paramètres d'entrée")
    status: str = Field(description="ok, warning ou fail")
    result: str = Field(description="Résultat textuel")
    ratio: str = Field(description="Ratio d'utilisation")
    code: str = Field(description="Clause norme appliquée")
    message: str = Field(default="", description="Message détaillé")


class ReportRequest(BaseModel):
    """Données d'entrée pour la génération d'un rapport PDF."""

    project_name: str = Field(default="Projet", description="Nom du projet")
    elements: list[ReportElement] = Field(description="Liste des éléments calculés")


@router.post(
    "/generate",
    summary="Générer un rapport PDF de vérification Eurocodes",
    description="Génère un PDF professionnel à partir des résultats de calculs structurels.",
)
async def generate_pdf(request: ReportRequest):
    """Génère un rapport PDF de vérification Eurocodes."""
    try:
        elements = [el.model_dump() for el in request.elements]
        pdf_path = generate_report(
            project_name=request.project_name,
            elements=elements,
        )
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"rapport_{request.project_name.lower().replace(' ', '_')}.pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
