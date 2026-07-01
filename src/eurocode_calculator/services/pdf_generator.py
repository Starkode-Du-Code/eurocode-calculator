"""Générateur PDF professionnel avec formules, tableaux et diagrammes."""

import io
import tempfile
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Backend non-interactif
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

_FONTS_DIR = Path(__file__).parent.parent / "fonts"

# Charte graphique
COLOR_PRIMARY = (37, 99, 235)   # Bleu
COLOR_SUCCESS = (34, 197, 94)   # Vert
COLOR_WARNING = (245, 158, 11)  # Orange
COLOR_DANGER = (239, 68, 68)    # Rouge
COLOR_TEXT = (30, 41, 59)       # Slate
COLOR_GRAY = (100, 116, 139)    # Slate secondaire
COLOR_LIGHT = (241, 245, 249)   # Fond gris


def _parse_ratio(ratio: str | float | int) -> float:
    """Convertit un ratio en float en gérant la virgule française."""
    if isinstance(ratio, (int, float)):
        return float(ratio)
    return float(str(ratio).replace(",", "."))


class EurocodePDF(FPDF):
    """PDF personnalisé avec charte graphique Eurocode Calculator."""

    def __init__(self) -> None:
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)

        # Polices Unicode
        self.add_font("DejaVu", "", str(_FONTS_DIR / "DejaVuSans.ttf"))
        self.add_font("DejaVu", "B", str(_FONTS_DIR / "DejaVuSans-Bold.ttf"))
        self.add_font("DejaVu", "I", str(_FONTS_DIR / "DejaVuSans-Oblique.ttf"))

    def header(self) -> None:
        """En-tête sur chaque page."""
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*COLOR_GRAY)
        self.cell(0, 10, "Eurocode Calculator v0.1.0 — API REST de vérification structurelle", align="L")
        self.cell(0, 10, f"Page {self.page_no()}", align="R")
        self.ln(15)

    def footer(self) -> None:
        """Pied de page."""
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*COLOR_GRAY)
        self.cell(0, 10, "Conforme EN 1992-1-1, EN 1993-1-1, EN 1997-1 | Document généré automatiquement", align="C")

    def add_title_page(self, project_name: str, date: str) -> None:
        """Page de titre professionnelle."""
        self.add_page()

        # Bandeau bleu
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(0, 0, 210, 60, "F")

        self.set_y(25)
        self.set_font("DejaVu", "B", 28)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, "Rapport de Vérification", align="C")
        self.ln(12)
        self.set_font("DejaVu", "", 16)
        self.cell(0, 10, "Eurocodes — Génie Civil Structurel", align="C")

        self.set_y(85)
        self.set_text_color(*COLOR_TEXT)
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, f"Projet : {project_name}", align="C")
        self.ln(8)
        self.set_font("DejaVu", "", 11)
        self.cell(0, 8, f"Date : {date}", align="C")
        self.ln(8)
        self.cell(0, 8, "Généré par Eurocode Calculator API", align="C")

        # Bloc résumé
        self.set_y(125)
        self.set_fill_color(*COLOR_LIGHT)
        self.rect(40, 125, 130, 55, "F")
        self.set_xy(50, 135)
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 8, "Résumé du rapport", align="L")
        self.ln(8)
        self.set_font("DejaVu", "", 10)
        self.set_text_color(*COLOR_TEXT)
        self.cell(0, 6, "• Vérification selon EN 1992-1-1 (Béton armé)", align="L")
        self.ln(6)
        self.cell(0, 6, "• Vérification selon EN 1993-1-1 (Acier)", align="L")
        self.ln(6)
        self.cell(0, 6, "• Vérification selon EN 1997-1 (Géotechnique)", align="L")

    def add_section_title(self, title: str, status: str = "ok") -> None:
        """Titre de section avec indicateur de statut."""
        if status == "ok":
            status_text = "[OK]"
            status_color = COLOR_SUCCESS
        elif status == "fail":
            status_text = "[NON OK]"
            status_color = COLOR_DANGER
        else:
            status_text = "[ATTENTION]"
            status_color = COLOR_WARNING

        self.set_font("DejaVu", "B", 14)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 12, title, align="L")

        # Indicateur de statut
        self.set_x(175)
        self.set_font("DejaVu", "B", 10)
        self.set_fill_color(*status_color)
        self.set_text_color(255, 255, 255)
        self.cell(25, 10, status_text, align="C", fill=True)
        self.ln(8)

        # Ligne bleue
        self.set_draw_color(*COLOR_PRIMARY)
        self.set_line_width(0.5)
        y = self.get_y()
        self.line(20, y, 190, y)
        self.ln(5)

    def add_formula(self, label: str, formula: str, result: str, unit: str = "") -> None:
        """Affiche une formule avec son résultat."""
        self.set_font("DejaVu", "I", 10)
        self.set_text_color(*COLOR_GRAY)
        self.cell(60, 8, label, align="L")

        self.set_font("DejaVu", "", 10)
        self.set_text_color(*COLOR_TEXT)
        self.cell(75, 8, formula, align="L")

        self.set_font("DejaVu", "B", 10)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(20, 8, f"= {result}", align="R")

        if unit:
            self.set_font("DejaVu", "", 9)
            self.set_text_color(*COLOR_GRAY)
            self.cell(0, 8, unit, align="R")
        self.ln(8)

    def add_inputs_table(self, inputs: dict[str, str]) -> None:
        """Tableau des données d'entrée."""
        self.set_fill_color(*COLOR_PRIMARY)
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 10)
        self.cell(70, 9, "Paramètre", border=1, fill=True, align="C")
        self.cell(0, 9, "Valeur", border=1, fill=True, align="C")
        self.ln()

        self.set_font("DejaVu", "", 10)
        self.set_text_color(*COLOR_TEXT)
        for param, value in inputs.items():
            self.cell(70, 8, param, border="LR")
            self.cell(0, 8, value, border="LR")
            self.ln()
        # Ligne de fermeture
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(5)

    def add_verification_table(self, checks: list[dict]) -> None:
        """Tableau de vérification avec codes couleur."""
        col_widths = [45, 55, 40, 20, 20]
        headers = ["Vérification", "Formule", "Résultat", "Ratio", "Statut"]

        # En-tête
        self.set_fill_color(*COLOR_PRIMARY)
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 9)
        for width, header in zip(col_widths, headers):
            self.cell(width, 10, header, border=1, fill=True, align="C")
        self.ln()

        # Lignes
        self.set_font("DejaVu", "", 9)
        for check in checks:
            status = check.get("status", "OK").upper()
            if status == "OK":
                status_color = COLOR_SUCCESS
            elif status == "WARNING":
                status_color = COLOR_WARNING
            else:
                status_color = COLOR_DANGER

            height = 10
            self.set_text_color(*COLOR_TEXT)

            # Vérification
            self.cell(col_widths[0], height, check.get("name", ""), border="LR", align="L")
            # Formule
            self.set_font("DejaVu", "I", 8)
            self.cell(col_widths[1], height, check.get("formula", ""), border="LR", align="L")
            self.set_font("DejaVu", "", 9)
            # Résultat
            self.cell(col_widths[2], height, check.get("result", ""), border="LR", align="C")
            # Ratio
            try:
                ratio = _parse_ratio(check.get("ratio", 0))
                if ratio <= 0.7:
                    self.set_text_color(*COLOR_SUCCESS)
                elif ratio <= 1.0:
                    self.set_text_color(*COLOR_WARNING)
                else:
                    self.set_text_color(*COLOR_DANGER)
                ratio_text = f"{ratio:.2f}"
            except (ValueError, TypeError):
                ratio_text = str(check.get("ratio", ""))
                self.set_text_color(*COLOR_TEXT)
            self.cell(col_widths[3], height, ratio_text, border="LR", align="C")
            self.set_text_color(*COLOR_TEXT)
            # Statut
            self.set_fill_color(*status_color)
            self.set_text_color(255, 255, 255)
            self.set_font("DejaVu", "B", 9)
            self.cell(col_widths[4], height, status, border=1, fill=True, align="C")
            self.set_fill_color(255, 255, 255)
            self.set_font("DejaVu", "", 9)
            self.ln()

        # Fermeture
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(5)

    def add_diagram(self, image_data: bytes, caption: str, width: float = 170) -> None:
        """Ajoute un diagramme matplotlib."""
        self.image(io.BytesIO(image_data), x=(210 - width) / 2, w=width)
        self.set_font("DejaVu", "I", 9)
        self.set_text_color(*COLOR_GRAY)
        self.cell(0, 6, f"Figure : {caption}", align="C")
        self.ln(8)


def generate_moment_diagram(L: float, q: float, M_Ed: float) -> bytes:
    """Génère le diagramme de moment fléchissant sous charge uniforme."""
    fig, ax = plt.subplots(figsize=(10, 4), dpi=150)

    x = np.linspace(0, L, 200)
    M = (q * L / 2) * x - (q * x**2) / 2

    ax.plot(x, M, color="#2563EB", linewidth=2.5, label="$M(x)$")
    ax.axhline(y=M_Ed, color="#EF4444", linestyle="--", linewidth=1.5, label=f"$M_{{Ed}} = {M_Ed:.1f}$ kN·m")
    ax.fill_between(x, 0, M, alpha=0.15, color="#2563EB")

    # Appuis
    ax.plot([0, 0], [0, -5], "k-", linewidth=4)
    ax.plot([L, L], [0, -5], "k-", linewidth=4)
    ax.plot([0], [-5], "k^", markersize=12)
    ax.plot([L], [-5], "k^", markersize=12)

    ax.set_xlabel("Portée $L$ [m]", fontsize=11)
    ax.set_ylabel("Moment $M$ [kN·m]", fontsize=11)
    ax.set_title("Diagramme de moment fléchissant — ELU", fontsize=12, fontweight="bold")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.5, L + 0.5)

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def generate_report(project_name: str, elements: list[dict]) -> Path:
    """
    Génère un rapport PDF professionnel.

    Args:
        project_name: Nom du projet affiché en page de titre.
        elements: Liste d'éléments avec inputs, calculations, checks, diagrams.

    Returns:
        Chemin vers le fichier PDF temporaire généré.
    """
    pdf = EurocodePDF()

    date = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.add_title_page(project_name, date)

    for elem in elements:
        pdf.add_page()
        pdf.add_section_title(f"{elem.get('type', 'Élément')} — {elem.get('name', '')}", elem.get("status", "ok"))

        # Données d'entrée
        pdf.set_font("DejaVu", "B", 11)
        pdf.set_text_color(*COLOR_TEXT)
        pdf.cell(0, 8, "Données d'entrée", align="L")
        pdf.ln(10)
        if elem.get("inputs"):
            pdf.add_inputs_table(elem["inputs"])

        # Calculs intermédiaires
        if elem.get("calculations"):
            pdf.set_font("DejaVu", "B", 11)
            pdf.cell(0, 8, "Calculs intermédiaires", align="L")
            pdf.ln(10)
            for calc in elem["calculations"]:
                pdf.add_formula(
                    calc.get("label", ""),
                    calc.get("formula", ""),
                    calc.get("result", ""),
                    calc.get("unit", ""),
                )
            pdf.ln(3)

        # Vérifications
        if elem.get("checks"):
            pdf.set_font("DejaVu", "B", 11)
            pdf.cell(0, 8, "Vérifications", align="L")
            pdf.ln(10)
            pdf.add_verification_table(elem["checks"])

        # Diagrammes
        if elem.get("diagrams"):
            for diag in elem["diagrams"]:
                image_data = generate_moment_diagram(
                    float(diag.get("L", 0)),
                    float(diag.get("q", 0)),
                    float(diag.get("M_Ed", 0)),
                )
                pdf.add_diagram(image_data, diag.get("caption", "Diagramme"))

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
        pdf.output(pdf_file.name)
        return Path(pdf_file.name)
