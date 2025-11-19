"""Initialize database with a test user."""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    # Check if user already exists
    existing_user = User.query.filter_by(username="testuser").first()
    if existing_user:
        print("Test user already exists!")
        print(f"Username: testuser")
        print("Password: testpass")
    else:
        # Create test user
        user = User(username="testuser", email="test@example.com")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()
        print("Test user created successfully!")
        print(f"Username: testuser")
        print("Password: testpass")




