from fastapi.testclient import TestClient
from app.core.config import settings


# 1. The Happy Path (Keep this)
def test_create_and_read_recipe(client: TestClient, normal_user_token_headers: dict):
    recipe_data = {
        "title": "Integration Test Pancakes",
        "description": "Fluffy",
        "ingredients": ["flour", "milk"],
    }
    response = client.post(
        f"{settings.API_V1_STR}/recipes/",
        headers=normal_user_token_headers,
        json=recipe_data,
    )
    assert response.status_code == 201
    created_id = response.json()["id"]

    # Verify we can read it back
    response = client.get(
        f"{settings.API_V1_STR}/recipes/{created_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Integration Test Pancakes"


# 2. The "Negative" Test (Security Check)
def test_delete_recipe_permission_denied(
    client: TestClient,
    normal_user_token_headers: dict,
    db,  # We use the db fixture to insert a "victim" recipe
):
    # Setup: Create a second user ("Attacker")
    attacker_email = "attacker@example.com"
    attacker_pass = "evilpass"
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": attacker_email, "password": attacker_pass},
    )

    # Login as Attacker
    resp = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": attacker_email, "password": attacker_pass},
    )
    attacker_headers = {"Authorization": f"Bearer {resp.json()['access_token']}"}

    # Setup: Normal User creates a recipe
    create_resp = client.post(
        f"{settings.API_V1_STR}/recipes/",
        headers=normal_user_token_headers,
        json={"title": "My Precious Recipe", "ingredients": []},
    )
    recipe_id = create_resp.json()["id"]

    # Act: Attacker tries to DELETE Normal User's recipe
    delete_resp = client.delete(
        f"{settings.API_V1_STR}/recipes/{recipe_id}", headers=attacker_headers
    )

    # Assert: Should be Forbidden (403)
    assert delete_resp.status_code == 403
    assert delete_resp.json()["detail"] == "Not enough permissions"
