"""User model for authentication and user management."""
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(UserMixin, db.Model):
    """User model representing the authenticated user/owner."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)

    # Calendar sync preferences
    calendar_sync_enabled = db.Column(db.Boolean, default=False, nullable=False)
    calendar_sync_mode = db.Column(
        db.String(20), default="manual", nullable=False
    )  # 'automatic' or 'manual'

    # CalDAV authentication
    caldav_username = db.Column(db.String(50), nullable=True)
    caldav_password_hash = db.Column(db.String(255), nullable=True)

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    last_login_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    journal_entries = db.relationship(
        "JournalEntry", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    calendar_events = db.relationship(
        "CalendarEvent", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        """Set password hash from plain text password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches the hash."""
        return check_password_hash(self.password_hash, password)

    def set_caldav_password(self, password):
        """Set CalDAV password hash from plain text password."""
        if password:
            self.caldav_password_hash = generate_password_hash(password)
        else:
            self.caldav_password_hash = None

    def check_caldav_password(self, password):
        """Check if provided CalDAV password matches the hash."""
        if not self.caldav_password_hash or not password:
            return False
        return check_password_hash(self.caldav_password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
