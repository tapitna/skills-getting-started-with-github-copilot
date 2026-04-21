import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    # Arrange
    # No special setup needed
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_activities():
    # Arrange
    # No special setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]

def test_signup_success():
    # Arrange
    email = "test@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "Signed up test@mergington.edu" in response.json()["message"]
    
    # Verify the participant was added
    response_get = client.get("/activities")
    data = response_get.json()
    assert email in data[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup?email={email}")  # First signup
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Invalid Activity"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success():
    # Arrange
    email = "unregister@mergington.edu"
    activity = "Gym Class"
    client.post(f"/activities/{activity}/signup?email={email}")  # Signup first
    
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered unregister@mergington.edu" in response.json()["message"]
    
    # Verify the participant was removed
    response_get = client.get("/activities")
    data = response_get.json()
    assert email not in data[activity]["participants"]

def test_unregister_not_signed_up():
    # Arrange
    email = "notsigned@mergington.edu"
    activity = "Basketball Team"
    
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Invalid Activity"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]