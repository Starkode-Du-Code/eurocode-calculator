"""Tests endpoint poutre EC2."""


def test_beam_verify_uls_ok(client):
    response = client.post(
        "/beam/verify-uls",
        json={
            "concrete_grade": "C30/37",
            "width_mm": 300,
            "height_mm": 500,
            "cover_mm": 30,
            "moment_knm": 50,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "verified" in data
    assert data["concrete_grade"] == "C30/37"
    assert data["fck_mpa"] > 0
    assert 0 < data["utilization_ratio"] < 2


def test_beam_verify_uls_fail(client):
    response = client.post(
        "/beam/verify-uls",
        json={
            "concrete_grade": "C25/30",
            "width_mm": 200,
            "height_mm": 300,
            "moment_knm": 500,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is False
    assert data["utilization_ratio"] > 1.0


def test_beam_invalid_dimensions(client):
    response = client.post(
        "/beam/verify-uls",
        json={"width_mm": -100, "height_mm": 500, "moment_knm": 50},
    )
    assert response.status_code == 422


def test_beam_verify_shear_ok(client):
    response = client.post(
        "/beam/verify-shear",
        json={
            "concrete_grade": "C30/37",
            "width_mm": 300,
            "height_mm": 500,
            "shear_force_kn": 50,
            "longitudinal_steel_area_mm2": 1256,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is True
    assert data["calculation_method"] == "capacity-based-structuralcodes"
    assert data["v_rdc_kn"] > 0


def test_beam_verify_shear_fail(client):
    response = client.post(
        "/beam/verify-shear",
        json={
            "concrete_grade": "C25/30",
            "width_mm": 200,
            "height_mm": 300,
            "shear_force_kn": 500,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is False


def test_beam_verify_shear_with_stirrups(client):
    response = client.post(
        "/beam/verify-shear",
        json={
            "concrete_grade": "C30/37",
            "width_mm": 300,
            "height_mm": 500,
            "shear_force_kn": 150,
            "stirrup_area_mm2": 100,
            "stirrup_spacing_mm": 150,
            "longitudinal_steel_area_mm2": 1256,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["v_rds_kn"] is not None
    assert data["v_rdmax_kn"] is not None


def test_beam_verify_capacity_ok(client):
    response = client.post(
        "/beam/verify-uls-capacity",
        json={
            "concrete_grade": "C30/37",
            "width_mm": 300,
            "height_mm": 500,
            "moment_knm": 40,
            "bottom_bar_diameter_mm": 20,
            "bottom_bar_count": 3,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is True
    assert data["moment_rd_knm"] > 0
    assert data["calculation_method"] == "capacity-based-structuralcodes"


def test_beam_verify_capacity_fail(client):
    response = client.post(
        "/beam/verify-uls-capacity",
        json={
            "concrete_grade": "C25/30",
            "width_mm": 200,
            "height_mm": 300,
            "moment_knm": 500,
            "bottom_bar_diameter_mm": 12,
            "bottom_bar_count": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is False
