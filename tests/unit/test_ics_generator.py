"""Unit tests for iCalendar generator service."""
import pytest
from datetime import date, datetime, timedelta


@pytest.fixture
def sample_entry(app, user):
    """Create a sample journal entry for testing."""
    with app.app_context():
        from models import db, JournalEntry
        entry = JournalEntry(
            user_id=user.id,
            title="Test Entry",
            content="This is a test entry content.",
            date=date.today(),
        )
        db.session.add(entry)
        db.session.commit()
        return entry


def test_truncate_text():
    """Test text truncation functionality."""
    from services.ics_generator import ICSGenerator
    long_text = "a" * 200
    truncated = ICSGenerator.truncate_text(long_text, 100)
    assert len(truncated) <= 103  # 100 + "..."
    assert truncated.endswith("...")


def test_strip_formatting():
    """Test formatting stripping functionality."""
    from services.ics_generator import ICSGenerator
    html_text = "<b>Bold</b> and <i>italic</i> text"
    stripped = ICSGenerator.strip_formatting(html_text)
    assert "<b>" not in stripped
    assert "<i>" not in stripped
    assert "Bold" in stripped
    assert "italic" in stripped


def test_generate_event_from_entry(sample_entry, app):
    """Test generating iCalendar event from journal entry."""
    from services.ics_generator import ICSGenerator
    with app.app_context():
        # Ensure entry is attached to session
        from models import db
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        event = ICSGenerator.generate_event_from_entry(sample_entry)
        assert event.name == "Test Entry"
        assert "test entry content" in event.description.lower()
        assert event.uid is not None


def test_generate_calendar_from_entries(sample_entry, app):
    """Test generating iCalendar calendar from entries."""
    from services.ics_generator import ICSGenerator
    with app.app_context():
        from models import db
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        entries = [sample_entry]
        calendar = ICSGenerator.generate_calendar_from_entries(entries)
        assert len(calendar.events) == 1


def test_generate_ics_string(sample_entry, app):
    """Test generating iCalendar string."""
    from services.ics_generator import ICSGenerator
    with app.app_context():
        from models import db
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        entries = [sample_entry]
        ics_string = ICSGenerator.generate_ics_string(entries)
        assert "BEGIN:VCALENDAR" in ics_string
        assert "END:VCALENDAR" in ics_string

