import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path

from app import app  # Import the Flask app

# --- Pytest Fixtures ---

@pytest.fixture
def client():
    """
    Fixture to provide a test client for Flask.
    Sets TESTING mode to True to get better error messages and disable error catching.
    """
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# --- Tests for Static Pages ---

def test_home_page(client):
    """
    Test that the home page loads correctly and contains expected text.
    """
    response = client.get('/')
    assert response.status_code == 200  # Ensure page loaded successfully
    assert b"Chicken Coop Tracker" in response.data  # Check that page contains specific content

# --- Tests for Egg Logs API ---

def test_add_egg_log(client, monkeypatch):
    """
    Test POSTing to the /api/eggs endpoint.
    Uses monkeypatch to prevent actual database commits.
    """
    def mock_commit():
        return None  # Do nothing instead of committing to DB
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    response = client.post('/api/eggs', json={'date': '2025-10-13', 'count': 5})
    assert response.status_code == 201  # Check success status code
    assert b'Egg log added successfully' in response.data  # Check response message

# --- Tests for Feed Logs API ---

def test_add_feed_log(client, monkeypatch):
    """
    Test POSTing to the /api/feed endpoint.
    Uses monkeypatch to prevent actual database commits.
    """
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    response = client.post('/api/feed', json={'date': '2025-10-13', 'amount': 2.5})
    assert response.status_code == 201
    assert b'Feed log added successfully' in response.data

# --- Tests for Water Logs API ---

def test_add_water_log(client, monkeypatch):
    """
    Test POSTing to the /api/water endpoint.
    Uses monkeypatch to prevent actual database commits.
    """
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    response = client.post('/api/water', json={'date': '2025-10-13', 'amount': 3.0})
    assert response.status_code == 201
    assert b'Water log added successfully' in response.data

# --- Tests for User Registration ---

def test_register_user(client, monkeypatch):
    """
    Test the user registration route.
    Uses monkeypatch to prevent actual database commits.
    Follows redirects to capture the flash message on the login page.
    """
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200  # Ensure page loaded after redirect
    # Check that the flash message for successful account creation is present
    assert b'Account created successfully! Please log in.' in response.data