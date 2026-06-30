"""Tests endpoint poteau EC3."""


def test_column_buckling_ok(client):
    response = client.post(
        "/column/buckling",
        json={
            "steel_grade": "S355",
            "profile_name": "HEA200",
            "length_mm": 3000,
            "axial_force_kn": 200,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "verified" in data
    assert data["steel_grade"] == "S355"
    assert data["slenderness"] > 0


def test_column_buckling_fail(client):
    response = client.post(
        "/column/buckling",
        json={
            "steel_grade": "S235",
            "profile_name": "HEA100",
            "length_mm": 8000,
            "axial_force_kn": 2000,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is False
