"""Unit tests for native app service."""
import pytest
from datetime import date


@pytest.fixture
def sample_entry(app, user):
    """Create a sample journal entry for testing."""
    with app.app_context():
        from models import db, JournalEntry
        entry = JournalEntry(
            user_id=user.id,
            title="Test Entry",
            content="Test content",
            date=date(2024, 1, 15),
        )
        db.session.add(entry)
        db.session.commit()
        return entry


def test_generate_calendar_url_with_entry(sample_entry, app):
    """Test generating calendar URL with entry."""
    from services.native_app_service import NativeAppService
    with app.app_context():
        from models import db
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        url = NativeAppService.generate_calendar_url(entry=sample_entry)
        assert url.startswith("calshow://")
        assert "20240115" in url


def test_generate_calendar_url_with_date():
    """Test generating calendar URL with date string."""
    from services.native_app_service import NativeAppService
    url = NativeAppService.generate_calendar_url(date="2024-01-15")
    assert url.startswith("calshow://")
    assert "20240115" in url


def test_generate_calendar_url_without_date():
    """Test generating calendar URL without date."""
    from services.native_app_service import NativeAppService
    url = NativeAppService.generate_calendar_url()
    assert url == "calshow://"


def test_generate_notes_url():
    """Test generating notes URL."""
    from services.native_app_service import NativeAppService
    url = NativeAppService.generate_notes_url()
    assert url == "mobilenotes://"


def test_generate_notes_url_with_entry(sample_entry, app):
    """Test generating notes URL with entry."""
    from services.native_app_service import NativeAppService
    with app.app_context():
        from models import db
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        url = NativeAppService.generate_notes_url(entry=sample_entry)
    assert url == "mobilenotes://"

