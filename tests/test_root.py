"""Tests for the root endpoint."""

from fastapi import status


def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows(client):
    """Test that following the redirect from / leads to the static directory."""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
