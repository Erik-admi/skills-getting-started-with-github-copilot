"""Unit tests for activity endpoints"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_all_activities_returns_dict(self, client):
        """Verify GET /activities returns a dictionary"""
        response = client.get("/activities")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    
    def test_get_activities_contains_expected_activities(self, client):
        """Verify returned activities include known activities"""
        response = client.get("/activities")
        activities = response.json()
        
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Swimming Club",
            "Art Club",
            "Drama Club",
            "Science Olympiad",
            "Robotics Club"
        ]
        
        for activity in expected_activities:
            assert activity in activities
    
    def test_activity_has_required_fields(self, client):
        """Verify each activity has all required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, \
                    f"Activity '{activity_name}' missing field '{field}'"
    
    def test_activity_participants_is_list(self, client):
        """Verify participants field is a list"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Participants for '{activity_name}' is not a list"
    
    def test_activity_max_participants_is_positive(self, client):
        """Verify max_participants is a positive integer"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"max_participants for '{activity_name}' is not an integer"
            assert activity_data["max_participants"] > 0, \
                f"max_participants for '{activity_name}' is not positive"
    
    def test_chess_club_has_initial_participants(self, client):
        """Verify Chess Club starts with pre-populated participants"""
        response = client.get("/activities")
        activities = response.json()
        
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestActivityData:
    """Tests for activity data structure and validation"""
    
    def test_all_activities_have_description(self, client):
        """Verify all activities have non-empty descriptions"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0
    
    def test_all_activities_have_schedule(self, client):
        """Verify all activities have non-empty schedules"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "schedule" in activity_data
            assert isinstance(activity_data["schedule"], str)
            assert len(activity_data["schedule"]) > 0
