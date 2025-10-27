import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# --- Home Page ---
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Chicken Coop Tracker" in response.data

# --- Egg Logs ---
def test_add_egg_log(client, monkeypatch):
    # Mock db.session.commit to prevent actual DB changes
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)
    
    response = client.post('/api/eggs', json={'date': '2025-10-13', 'count': 5})
    assert response.status_code == 201
    assert b'Egg log added successfully' in response.data

# --- Feed Logs ---
def test_add_feed_log(client, monkeypatch):
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    response = client.post('/api/feed', json={'date': '2025-10-13', 'amount': 2.5})
    assert response.status_code == 201
    assert b'Feed log added successfully' in response.data

# --- Water Logs ---
def test_add_water_log(client, monkeypatch):
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    response = client.post('/api/water', json={'date': '2025-10-13', 'amount': 3.0})
    assert response.status_code == 201
    assert b'Water log added successfully' in response.data