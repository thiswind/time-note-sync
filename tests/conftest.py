"""Pytest configuration and shared fixtures."""
import pytest
import sys
import os

# Add root directory to path for imports (monolithic Flask structure)
root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_path)

from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app("testing")
    # app.py already creates tables in create_app
    yield app
    # Clean up after tests - no need to drop, using in-memory database


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def user(app):
    """Create a test user."""
    with app.app_context():
        # Import using relative imports (same as test_db.py which works)
        from models import db, User
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()
        # Refresh to get the ID
        db.session.refresh(user)
        return user


@pytest.fixture
def auth_headers(client, user):
    """Get authentication headers for API requests."""
    # Login to get session
    response = client.post(
        '/api/auth/login',
        json={'username': 'testuser', 'password': 'testpass'},
        content_type='application/json'
    )
    assert response.status_code == 200
    
    # Return cookies for authenticated requests
    return {'Cookie': response.headers.get('Set-Cookie', '')}

