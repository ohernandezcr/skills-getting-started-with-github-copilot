from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"

    response = client.post(
        f"/activities/{activity_name}/signup?email=student@mergington.edu"
    )
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")

    remove_response = client.delete(
        f"/activities/{activity_name}/unregister?email=student@mergington.edu"
    )
    assert remove_response.status_code == 200
    assert remove_response.json()["message"].startswith("Removed")

    final_response = client.get("/activities")
    activity = final_response.json()[activity_name]
    assert "student@mergington.edu" not in activity["participants"]
