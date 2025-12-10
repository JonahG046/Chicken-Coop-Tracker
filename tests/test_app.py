import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# --- Pytest Fixtures ---

@pytest.fixture
def client():
    """
    Fixture to provide a test client for Flask.
    """
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# --- Tests for Static Pages ---

def test_home_page_redirects_to_login(client):
    """
    Home page should redirect to login if not logged in.
    """
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

# --- Tests for Egg Logs API ---

def test_add_egg_log(client, monkeypatch):
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.post('/api/eggs', json={'date': '2025-10-13', 'count': 5})
    assert response.status_code == 201
    assert b'Egg log added successfully' in response.data

# --- Tests for Feed Logs API ---

def test_add_feed_log(client, monkeypatch):
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.post('/api/feed', json={'date': '2025-10-13', 'amount': 2.5})
    assert response.status_code == 201
    assert b'Feed log added successfully' in response.data

# --- Tests for Water Logs API ---

def test_add_water_log(client, monkeypatch):
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.post('/api/water', json={'date': '2025-10-13', 'amount': 3.0})
    assert response.status_code == 201
    assert b'Water log added successfully' in response.data

# --- Tests for User Registration ---

def test_register_user(client, monkeypatch):
    def mock_commit():
        return None
    monkeypatch.setattr('app.db.session.commit', mock_commit)

    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created successfully! Please log in.' in response.data

# --- Tests for User Login/Logout ---


def test_logout(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out.' in response.data
    with client.session_transaction() as sess:
        assert 'user_id' not in sess

# --- Tests for Access Control ---

def test_protected_pages_redirect_when_not_logged_in(client):
    protected_urls = ['/', '/feed', '/water', '/eggs', '/settings']
    for url in protected_urls:
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data

# --- Tests for API access control ---

def test_get_egg_logs_redirect_if_not_logged_in(client):
    response = client.get('/api/eggs')
    assert response.status_code == 401
    assert b'You must be logged in' in response.data

def test_get_feed_logs_redirect_if_not_logged_in(client):
    response = client.get('/api/feed')
    assert response.status_code == 401
    assert b'You must be logged in' in response.data

def test_get_water_logs_redirect_if_not_logged_in(client):
    response = client.get('/api/water')
    assert response.status_code == 401
    assert b'You must be logged in' in response.data