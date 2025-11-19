"""Database models and initialization."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .journal_entry import JournalEntry
from .calendar_event import CalendarEvent

__all__ = ["db", "User", "JournalEntry", "CalendarEvent"]




