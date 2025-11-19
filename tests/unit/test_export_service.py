"""Unit tests for export service."""
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
            content="This is a test entry content.",
            date=date.today(),
        )
        db.session.add(entry)
        db.session.commit()
        return entry


def test_format_entry_for_notes(sample_entry, app):
    """Test formatting entry for Notes export."""
    from services.export_service import ExportService
    with app.app_context():
        from models import db
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        formatted = ExportService.format_entry_for_notes(sample_entry)
        assert "Test Entry" in formatted
        assert "test entry content" in formatted.lower()
        assert "日期:" in formatted


def test_generate_shortcuts_url_single(sample_entry, app):
    """Test generating Shortcuts URL for single entry."""
    from services.export_service import ExportService
    with app.app_context():
        from models import db
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        url = ExportService.generate_shortcuts_url([sample_entry])
        assert url.startswith("shortcuts://")
        assert "run-shortcut" in url


def test_export_single_entry(sample_entry, app):
    """Test exporting single entry."""
    from services.export_service import ExportService
    with app.app_context():
        from models import db
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        url = ExportService.export_single_entry(sample_entry)
        assert url.startswith("shortcuts://")


def test_export_multiple_entries(sample_entry, app):
    """Test exporting multiple entries."""
    from services.export_service import ExportService
    with app.app_context():
        from models import db, JournalEntry
        db.session.add(sample_entry)
        db.session.refresh(sample_entry)
        entry2 = JournalEntry(
            user_id=sample_entry.user_id,
            title="Second Entry",
            content="Second content.",
            date=date.today(),
        )
        db.session.add(entry2)
        db.session.commit()
        url = ExportService.export_multiple_entries([sample_entry, entry2])
        assert url.startswith("shortcuts://")


def test_export_empty_list():
    """Test exporting empty list raises error."""
    from services.export_service import ExportService
    with pytest.raises(ValueError):
        ExportService.export_multiple_entries([])

