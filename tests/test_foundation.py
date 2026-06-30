"""Tests endpoint fondation EC7."""


def test_foundation_bearing_ok(client):
    response = client.post(
        "/foundation/bearing",
        json={
            "soil_type": "dense_sand",
            "foundation_width_m": 2.0,
            "foundation_length_m": 2.0,
            "vertical_load_kn": 500,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is True
    assert data["foundation_area_m2"] == 4.0


def test_foundation_bearing_fail(client):
    response = client.post(
        "/foundation/bearing",
        json={
            "soil_type": "soft_clay",
            "foundation_width_m": 1.0,
            "foundation_length_m": 1.0,
            "vertical_load_kn": 100,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is False
