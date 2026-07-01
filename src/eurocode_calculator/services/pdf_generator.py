"""Génération de rapports PDF de vérification Eurocodes."""

import tempfile
from datetime import datetime
from pathlib import Path

from fpdf import FPDF
from jinja2 import Environment, FileSystemLoader

# Répertoire contenant les templates Jinja2
_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_FONTS_DIR = Path(__file__).parent.parent / "fonts"
_jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR), autoescape=True)


def generate_report(project_name: str, elements: list[dict]) -> Path:
    """
    Génère un rapport PDF à partir d'un template Jinja2 et le retourne sous forme de fichier temporaire.

    Args:
        project_name: Nom du projet affiché en en-tête.
        elements: Liste d'éléments structurés avec type, name, inputs, status, result, ratio, code, message.

    Returns:
        Chemin vers le fichier PDF généré.
    """
    template = _jinja_env.get_template("report.html")
    html = template.render(
        project_name=project_name,
        elements=elements,
        date=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("NotoSans", "", str(_FONTS_DIR / "NotoSans-Regular.ttf"))
    pdf.add_font("NotoSans", "B", str(_FONTS_DIR / "NotoSans-Bold.ttf"))
    pdf.set_font("NotoSans", size=11)
    pdf.add_page()
    pdf.write_html(html)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
        pdf.output(pdf_file.name)
        return Path(pdf_file.name)
