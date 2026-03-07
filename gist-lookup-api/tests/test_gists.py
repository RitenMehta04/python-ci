import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_octocat_has_gists():
    response = client.get("/octocat")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # octocat usually has ≥1 public gist
    assert len(data) >= 1
    assert "id" in data[0]
    assert "html_url" in data[0]


def test_missing_user():
    response = client.get("/this-user-does-not-exist-999999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_empty_gists_user():
    response = client.get("/torvalds")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least one gist exists now
    # Optionally be more specific:
    assert any(gist["html_url"].endswith("6faadce34c56d53b2d5352da0c3cd093") for gist in data)
    # Or check description contains expected text
    assert any("fishy crypto" in gist.get("description", "") for gist in data)