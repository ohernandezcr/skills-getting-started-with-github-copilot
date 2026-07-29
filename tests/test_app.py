from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    final_response = client.get("/activities")
    activity = final_response.json()[activity_name]

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json()["message"].startswith("Signed up")

    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"].startswith("Removed")

    assert email not in activity["participants"]


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    # Act
    first_signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    final_response = client.get("/activities")
    activity = final_response.json()[activity_name]
    cleanup_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert first_signup_response.status_code == 200
    assert second_signup_response.status_code == 400
    assert second_signup_response.json()["detail"] == "Student is already signed up for this activity"
    assert activity["participants"].count(email) == 1
    assert cleanup_response.status_code == 200
