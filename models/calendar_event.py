"""Calendar Event model for CalDAV calendar events."""
from datetime import datetime, timezone
from . import db


class CalendarEvent(db.Model):
    """Calendar Event model representing a calendar event synced from/to iPhone Calendar."""

    __tablename__ = "calendar_events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    external_event_id = db.Column(
        db.String(255), unique=True, nullable=False, index=True
    )  # CalDAV UID
    journal_entry_id = db.Column(
        db.Integer, db.ForeignKey("journal_entries.id"), nullable=True, index=True
    )

    # Event details
    title = db.Column(db.String(200), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.Text, nullable=True)
    completion_status = db.Column(
        db.String(20), nullable=True
    )  # 'not_started', 'in_progress', 'completed', 'cancelled'
    notes = db.Column(db.Text, nullable=True)

    # Sync metadata
    sync_direction = db.Column(
        db.String(20), nullable=False
    )  # 'web_to_iphone', 'iphone_to_web', 'bidirectional'
    last_synced_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    def to_dict(self):
        """Convert calendar event to dictionary."""
        return {
            "id": self.id,
            "external_event_id": self.external_event_id,
            "journal_entry_id": self.journal_entry_id,
            "title": self.title,
            "start_datetime": self.start_datetime.isoformat()
            if self.start_datetime
            else None,
            "end_datetime": self.end_datetime.isoformat()
            if self.end_datetime
            else None,
            "description": self.description,
            "completion_status": self.completion_status,
            "notes": self.notes,
            "sync_direction": self.sync_direction,
            "last_synced_at": self.last_synced_at.isoformat()
            if self.last_synced_at
            else None,
        }

    def __repr__(self):
        return f"<CalendarEvent {self.id}: {self.title[:50]}>"
