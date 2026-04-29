"""Fixtures and configuration for FastAPI backend tests"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to known state before each test
    
    This fixture ensures test isolation by resetting the in-memory
    activities database to a clean state before each test runs.
    Automatically applied to all tests (autouse=True).
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice basketball skills and compete in school leagues",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim laps, improve technique, and join swim meets",
            "schedule": "Mondays, Wednesdays, 4:30 PM - 6:00 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
        },
        "Drama Club": {
            "description": "Develop acting skills and put on school performances",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["chloe@mergington.edu", "jack@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Prepare for science competitions with hands-on experiments",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["amelia@mergington.edu", "logan@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build robots, learn engineering, and compete in challenges",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["sophia@mergington.edu", "mason@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_email():
    """Provide a sample email for signup tests"""
    return "newstudent@mergington.edu"


@pytest.fixture
def sample_activity_name():
    """Provide a sample activity name for tests"""
    return "Chess Club"
