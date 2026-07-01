"""Tests du générateur de rapports PDF."""

import pytest

from eurocode_calculator.services.pdf_generator import generate_report


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
        },
        {
            "type": "Poteau",
            "name": "C1",
            "inputs": {"Ned": "1500 kN", "My": "120 kN.m"},
            "status": "fail",
            "result": "Non vérifié",
            "ratio": "1.12",
            "code": "EN 1993-1-1",
            "message": "Le ratio dépasse la limite de 1.0.",
        },
    ]


def test_generate_report_creates_pdf(sample_elements):
    path = generate_report("Projet Test", sample_elements)
    assert path.exists()
    assert path.suffix == ".pdf"
    assert path.stat().st_size > 0
    # Le fichier commence par la signature PDF
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
