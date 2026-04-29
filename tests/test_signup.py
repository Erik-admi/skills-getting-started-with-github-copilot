"""Unit tests for signup and unregister endpoints"""

import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_student_succeeds(self, client, sample_activity_name, sample_email):
        """Verify a new student can sign up for activity"""
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 200
        assert "message" in response.json()
        assert sample_email in response.json()["message"]
    
    def test_signup_adds_participant_to_activity(self, client, sample_activity_name, sample_email):
        """Verify signup adds student to participants list"""
        # Get initial participant count
        response = client.get("/activities")
        initial_count = len(response.json()[sample_activity_name]["participants"])
        
        # Sign up new student
        client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        
        # Verify participant was added
        response = client.get("/activities")
        new_count = len(response.json()[sample_activity_name]["participants"])
        
        assert new_count == initial_count + 1
        assert sample_email in response.json()[sample_activity_name]["participants"]
    
    def test_signup_nonexistent_activity_returns_404(self, client, sample_email):
        """Verify signup fails for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_duplicate_email_fails(self, client, sample_activity_name):
        """Verify duplicate signup is rejected"""
        duplicate_email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": duplicate_email}
        )
        
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_response_format(self, client, sample_activity_name, sample_email):
        """Verify signup response has correct format"""
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)


class TestMultipleSignups:
    """Tests for multiple signup scenarios"""
    
    def test_multiple_students_can_signup_for_same_activity(self, client, sample_activity_name):
        """Verify multiple different students can sign up"""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        response1 = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email2}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both are registered
        response = client.get("/activities")
        participants = response.json()[sample_activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants
    
    def test_student_can_signup_for_multiple_activities(self, client, sample_email):
        """Verify same student can sign up for different activities"""
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": sample_email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": sample_email}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify student is in both activities
        response = client.get("/activities")
        activities = response.json()
        assert sample_email in activities[activity1]["participants"]
        assert sample_email in activities[activity2]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""
    
    def test_unregister_existing_participant_succeeds(self, client, sample_activity_name):
        """Verify registered student can unregister"""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.delete(
            f"/activities/{sample_activity_name}/participants/{email}"
        )
        
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Unregistered" in response.json()["message"]
    
    def test_unregister_removes_participant(self, client, sample_activity_name):
        """Verify unregister removes student from participants list"""
        email = "michael@mergington.edu"
        
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()[sample_activity_name]["participants"])
        
        # Unregister
        client.delete(
            f"/activities/{sample_activity_name}/participants/{email}"
        )
        
        # Verify participant was removed
        response = client.get("/activities")
        new_count = len(response.json()[sample_activity_name]["participants"])
        
        assert new_count == initial_count - 1
        assert email not in response.json()[sample_activity_name]["participants"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Verify unregister fails for non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Club/participants/student@example.com"
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_nonexistent_participant_returns_404(self, client, sample_activity_name):
        """Verify unregister fails if student not registered"""
        response = client.delete(
            f"/activities/{sample_activity_name}/participants/notregistered@mergington.edu"
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_then_signup_again_succeeds(self, client, sample_activity_name, sample_email):
        """Verify student can signup after unregistering"""
        # Sign up
        client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        
        # Unregister
        client.delete(
            f"/activities/{sample_activity_name}/participants/{sample_email}"
        )
        
        # Sign up again
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 200
