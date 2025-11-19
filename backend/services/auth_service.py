"""Authentication service for user authentication and authorization."""
import logging
from flask import session
from flask_login import login_user, logout_user, current_user
from models import db, User

logger = logging.getLogger(__name__)


class AuthService:
    """Service for handling authentication and authorization."""

    @staticmethod
    def authenticate(username, password):
        """
        Authenticate a user with username and password.

        Args:
            username: Username
            password: Plain text password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            logger.info(f"User {username} authenticated successfully")
            return user
        logger.warning(f"Authentication failed for username: {username}")
        return None

    @staticmethod
    def login(user, remember=False):
        """
        Log in a user and create a session.

        Args:
            user: User object to log in
            remember: Whether to remember the user session

        Returns:
            True if login successful
        """
        if login_user(user, remember=remember):
            user.last_login_at = db.func.now()
            db.session.commit()
            logger.info(f"User {user.username} logged in")
            return True
        return False

    @staticmethod
    def logout():
        """Log out the current user."""
        if current_user.is_authenticated:
            username = current_user.username
            logout_user()
            logger.info(f"User {username} logged out")
            return True
        return False

    @staticmethod
    def require_owner(user_id):
        """
        Check if current user is the owner of a resource.

        Args:
            user_id: ID of the user who owns the resource

        Returns:
            True if current user is the owner, False otherwise
        """
        if not current_user.is_authenticated:
            logger.warning("Unauthenticated user attempted to access resource")
            return False

        if current_user.id != user_id:
            logger.warning(
                f"User {current_user.username} attempted to access resource owned by user {user_id}"
            )
            return False

        return True

    @staticmethod
    def create_user(username, password, email=None):
        """
        Create a new user account.

        Args:
            username: Username
            password: Plain text password
            email: Optional email address

        Returns:
            User object if created successfully, None otherwise
        """
        if User.query.filter_by(username=username).first():
            logger.warning(f"Attempt to create user with existing username: {username}")
            return None

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logger.info(f"User {username} created successfully")
        return user
