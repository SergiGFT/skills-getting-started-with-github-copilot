from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_delete_participant():
    activity = "Chess Club"
    email = "pytest-test@example.com"

    # ensure not present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    if email in participants:
        # cleanup if leftover from earlier runs
        client.delete(f"/activities/{activity}/participants?email={email}")

    # signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in resp.json()["message"]

    # verify present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # delete
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email in resp.json()["message"]

    # verify removed
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants


def test_signup_already_exists():
    activity = "Chess Club"
    # michael@mergington.edu is in the seed data
    resp = client.post(f"/activities/{activity}/signup?email=michael@mergington.edu")
    assert resp.status_code == 400


def test_delete_nonexistent_participant():
    activity = "Chess Club"
    email = "nonexistent@example.com"
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 404
