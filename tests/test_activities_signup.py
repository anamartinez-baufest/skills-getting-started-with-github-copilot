"""Tests for the POST /activities/{activity_name}/signup endpoint."""

from fastapi import status


def test_signup_for_activity_success(client):
    """Test successful signup for an activity."""
    email = "newstudent@mergington.edu"
    response = client.post(
        "/activities/Soccer Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == f"Signed up {email} for Soccer Club"
    
    # Verify the student was added
    activities = client.get("/activities").json()
    assert email in activities["Soccer Club"]["participants"]


def test_signup_for_activity_not_found(client):
    """Test signup for a non-existent activity."""
    response = client.post(
        "/activities/Non-existent Club/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_duplicate_student(client):
    """Test that a student cannot sign up twice for the same activity."""
    email = "michael@mergington.edu"  # Already in Chess Club
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_multiple_activities_same_student(client):
    """Test that a student can sign up for multiple different activities."""
    email = "newstudent@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        "/activities/Soccer Club/signup",
        params={"email": email}
    )
    assert response1.status_code == status.HTTP_200_OK
    
    # Sign up for second activity
    response2 = client.post(
        "/activities/Art Club/signup",
        params={"email": email}
    )
    assert response2.status_code == status.HTTP_200_OK
    
    # Verify student is in both activities
    activities = client.get("/activities").json()
    assert email in activities["Soccer Club"]["participants"]
    assert email in activities["Art Club"]["participants"]


def test_signup_preserves_existing_participants(client):
    """Test that signing up a new student preserves existing participants."""
    email = "newstudent@mergington.edu"
    
    # Get initial participants for Chess Club
    initial = client.get("/activities").json()
    initial_participants = initial["Chess Club"]["participants"].copy()
    
    # Sign up new student for different activity
    client.post(
        "/activities/Soccer Club/signup",
        params={"email": email}
    )
    
    # Verify Chess Club participants unchanged
    final = client.get("/activities").json()
    assert final["Chess Club"]["participants"] == initial_participants


def test_signup_with_empty_email(client):
    """Test signup with empty email parameter."""
    response = client.post(
        "/activities/Soccer Club/signup",
        params={"email": ""}
    )
    
    # Empty email is technically valid for the current implementation
    # but this test documents the behavior
    if response.status_code == status.HTTP_200_OK:
        activities = client.get("/activities").json()
        assert "" in activities["Soccer Club"]["participants"]


def test_signup_with_special_characters_in_email(client):
    """Test signup with special characters in email."""
    email = "student+tag@mergington.edu"
    response = client.post(
        "/activities/Art Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == status.HTTP_200_OK
    activities = client.get("/activities").json()
    assert email in activities["Art Club"]["participants"]


def test_signup_case_sensitive_activity_name(client):
    """Test that activity names are case-sensitive."""
    response = client.post(
        "/activities/soccer club/signup",  # lowercase
        params={"email": "student@mergington.edu"}
    )
    
    # Should not find "soccer club" (case-sensitive)
    assert response.status_code == status.HTTP_404_NOT_FOUND
