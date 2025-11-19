"""Journal Entry model for journal entries."""
from datetime import datetime, date, timezone
from . import db


class JournalEntry(db.Model):
    """Journal Entry model representing a single journal entry."""

    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )  # Indexed for user-based queries (T107)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)  # Indexed for date-based queries (T107)

    # Calendar sync fields
    calendar_event_id = db.Column(db.String(255), nullable=True, index=True)  # Indexed for calendar sync queries (T107)
    sync_status = db.Column(
        db.String(20),
        default="not_synced",
        nullable=False,
        index=True,
    )  # 'not_synced', 'synced', 'sync_pending', 'sync_conflict' - Indexed for sync status queries (T107)
    completion_status = db.Column(
        db.String(20), nullable=True
    )  # 'not_started', 'in_progress', 'completed', 'cancelled'

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    calendar_event = db.relationship(
        "CalendarEvent",
        backref="journal_entry",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        """Convert journal entry to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "date": self.date.isoformat() if self.date else None,
            "calendar_event_id": self.calendar_event_id,
            "sync_status": self.sync_status,
            "completion_status": self.completion_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<JournalEntry {self.id}: {self.title[:50]}>"
