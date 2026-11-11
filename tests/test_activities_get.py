"""Tests for the GET /activities endpoint."""

from fastapi import status


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == status.HTTP_200_OK
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9
    
    # Verify expected activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Club",
        "Track and Field",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club"
    ]
    for activity in expected_activities:
        assert activity in activities


def test_get_activities_has_correct_structure(client):
    """Test that each activity has the required fields."""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
        assert required_fields.issubset(
            activity_data.keys()
        ), f"{activity_name} missing required fields"
        
        # Verify field types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        assert all(isinstance(p, str) for p in activity_data["participants"])


def test_get_activities_has_participants(client):
    """Test that activities with participants show them correctly."""
    response = client.get("/activities")
    activities = response.json()
    
    # Chess Club should have participants
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Soccer Club should have no participants
    assert activities["Soccer Club"]["participants"] == []


def test_get_activities_content_type(client):
    """Test that the response has the correct content type."""
    response = client.get("/activities")
    assert response.headers["content-type"] == "application/json"
