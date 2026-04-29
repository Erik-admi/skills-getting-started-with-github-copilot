"""Unit tests for data operations and storage"""

import pytest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import activities


class TestActivityDataStructure:
    """Tests for activity data structure and initialization"""
    
    def test_activities_dict_not_empty(self):
        """Verify activities database is initialized with data"""
        assert len(activities) > 0
    
    def test_nine_activities_initialized(self):
        """Verify exactly 9 activities are initialized"""
        assert len(activities) == 9
    
    def test_activities_keys_are_strings(self):
        """Verify all activity names (keys) are strings"""
        for activity_name in activities.keys():
            assert isinstance(activity_name, str)
            assert len(activity_name) > 0
    
    def test_activities_values_are_dicts(self):
        """Verify all activity values are dictionaries"""
        for activity_data in activities.values():
            assert isinstance(activity_data, dict)


class TestParticipantOperations:
    """Tests for participant list operations"""
    
    def test_participants_list_operations(self, reset_activities):
        """Verify basic list operations on participants"""
        activity_name = "Chess Club"
        activity = activities[activity_name]
        
        initial_count = len(activity["participants"])
        
        # Append a participant
        test_email = "testuser@mergington.edu"
        activity["participants"].append(test_email)
        
        assert len(activity["participants"]) == initial_count + 1
        assert test_email in activity["participants"]
    
    def test_participants_removal(self, reset_activities):
        """Verify participant removal works correctly"""
        activity_name = "Chess Club"
        activity = activities[activity_name]
        
        email_to_remove = "michael@mergington.edu"
        initial_count = len(activity["participants"])
        
        # Remove a participant
        activity["participants"].remove(email_to_remove)
        
        assert len(activity["participants"]) == initial_count - 1
        assert email_to_remove not in activity["participants"]
    
    def test_participant_unique_emails(self, reset_activities):
        """Verify each participant email is unique (no duplicates)"""
        activity_name = "Chess Club"
        activity = activities[activity_name]
        
        participants = activity["participants"]
        unique_participants = set(participants)
        
        assert len(participants) == len(unique_participants), \
            "Participants list contains duplicate emails"
    
    def test_all_activities_have_no_duplicate_participants(self):
        """Verify no activity has duplicate participants"""
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            unique_participants = set(participants)
            
            assert len(participants) == len(unique_participants), \
                f"Activity '{activity_name}' has duplicate participants"


class TestDataReset:
    """Tests for data reset and isolation"""
    
    def test_activities_reset_fixture_isolates_tests(self, client):
        """Verify that test isolation works via reset fixture"""
        # Get initial state
        response1 = client.get("/activities")
        chess_club_1 = response1.json()["Chess Club"]
        initial_participants = chess_club_1["participants"].copy()
        
        # The fixture should reset activities between tests
        # This test verifies the fixture works by checking reset state
        assert len(initial_participants) == 2
        assert "michael@mergington.edu" in initial_participants
    
    def test_modifications_dont_persist_between_test_runs(self):
        """Verify activities are in known state at start of each test"""
        # All tests should start with Chess Club having exactly 2 participants
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2


class TestActivityConstraints:
    """Tests for activity constraints like max participants"""
    
    def test_all_activities_respect_max_participants(self):
        """Verify participant count does not exceed max_participants"""
        for activity_name, activity_data in activities.items():
            participants_count = len(activity_data["participants"])
            max_participants = activity_data["max_participants"]
            
            assert participants_count <= max_participants, \
                f"Activity '{activity_name}' has {participants_count} participants " \
                f"but max is {max_participants}"
    
    def test_max_participants_positive_integers(self):
        """Verify max_participants are positive integers"""
        for activity_name, activity_data in activities.items():
            max_participants = activity_data["max_participants"]
            
            assert isinstance(max_participants, int), \
                f"max_participants for '{activity_name}' is not an integer"
            assert max_participants > 0, \
                f"max_participants for '{activity_name}' is not positive"
    
    def test_min_max_participants_is_at_least_10(self):
        """Verify no activity has fewer than 10 max participants"""
        for activity_name, activity_data in activities.items():
            assert activity_data["max_participants"] >= 10, \
                f"Activity '{activity_name}' has only {activity_data['max_participants']} max participants"
