"""Tests du générateur de rapports PDF."""

import pytest

from eurocode_calculator.services.pdf_generator import generate_moment_diagram, generate_report


@pytest.fixture
def sample_elements():
    return [
        {
            "type": "Poutre",
            "name": "P1",
            "inputs": {"b": "300 mm", "h": "500 mm", "fcd": "20 MPa"},
            "status": "ok",
            "result": "Vérifié",
            "ratio": "0.85",
            "code": "EN 1992-1-1",
            "message": "Le moment résistant est supérieur au moment sollicitant.",
            "calculations": [
                {"label": "Charge", "formula": "q = g + q", "result": "40", "unit": "kN/m"},
            ],
            "checks": [
                {
                    "name": "Flexion",
                    "formula": "MEd ≤ MRd",
                    "result": "150 ≤ 200",
                    "ratio": "0.75",
                    "status": "OK",
                },
            ],
            "diagrams": [
                {"L": 6.0, "q": 40.0, "M_Ed": 150.0, "caption": "Moment ELU"},
            ],
        },
        {
            "type": "Poteau",
            "name": "C1",
            "inputs": {"Ned": "1500 kN", "My": "120 kN.m"},
            "status": "fail",
            "result": "Non vérifié",
            "ratio": "1,12",
            "code": "EN 1993-1-1",
            "message": "Le ratio dépasse la limite de 1.0.",
        },
    ]


def test_generate_report_creates_pdf(sample_elements):
    path = generate_report("Projet Test", sample_elements)
    assert path.exists()
    assert path.suffix == ".pdf"
    assert path.stat().st_size > 0
    assert path.read_bytes()[:4] == b"%PDF"


def test_report_endpoint(client, sample_elements):
    response = client.post("/report/generate", json={"project_name": "Projet Test", "elements": sample_elements})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"].startswith('attachment; filename="rapport_projet_test.pdf"')
    assert response.content[:4] == b"%PDF"


def test_report_endpoint_empty_elements(client):
    response = client.post("/report/generate", json={"project_name": "Vide", "elements": []})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content[:4] == b"%PDF"


def test_report_endpoint_missing_field(client):
    response = client.post("/report/generate", json={"project_name": "Incomplet"})
    assert response.status_code == 422


def test_report_demo_endpoint(client):
    response = client.post("/report/demo")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    disposition = response.headers["content-disposition"]
    assert disposition.startswith('attachment; filename="Rapport_Verification_Poutre_RDC.pdf"')
    assert response.content[:4] == b"%PDF"
    assert len(response.content) > 10000  # Le PDF avec diagramme est significativement plus lourd


def test_generate_moment_diagram():
    image = generate_moment_diagram(L=6.0, q=40.0, M_Ed=150.0)
    assert image.startswith(b"\x89PNG")
