import pytest


def test_get_activities_returns_seed_data(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"]


def test_signup_adds_participant_and_updates_list(client):
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    post_response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert post_response.status_code == 200
    assert email in post_response.json()["message"]

    updated = client.get("/activities").json()
    assert email in updated[activity]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    activity = "Chess Club"
    email = "duplicate@mergington.edu"

    first = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert first.status_code == 200

    second = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert second.status_code == 400
    assert "already signed" in second.json()["detail"].lower()


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": "x@y.com"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_removes_participant(client):
    activity = "Programming Class"
    existing_email = client.get("/activities").json()[activity]["participants"][0]

    delete_response = client.delete(f"/activities/{activity}/unregister", params={"email": existing_email})
    assert delete_response.status_code == 200
    assert existing_email in delete_response.json()["message"]

    updated = client.get("/activities").json()
    assert existing_email not in updated[activity]["participants"]


def test_unregister_missing_participant_returns_404(client):
    activity = "Programming Class"
    missing_email = "missing@mergington.edu"

    delete_response = client.delete(f"/activities/{activity}/unregister", params={"email": missing_email})
    assert delete_response.status_code == 404
    assert "not found" in delete_response.json()["detail"].lower()


def test_unregister_unknown_activity_returns_404(client):
    delete_response = client.delete("/activities/Unknown Club/unregister", params={"email": "x@y.com"})
    assert delete_response.status_code == 404
    assert "not found" in delete_response.json()["detail"].lower()
