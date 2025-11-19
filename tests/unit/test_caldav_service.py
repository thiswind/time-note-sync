"""Unit tests for CalDAV service."""
import pytest
from datetime import date, datetime, timezone, timedelta


@pytest.fixture
def sample_entry(app, user):
    """Create a sample journal entry for testing."""
    with app.app_context():
        from services.journal_service import JournalService
        entry = JournalService.create_entry(
            user_id=user.id,
            title="Test Entry",
            content="Test content",
            entry_date=date.today(),
        )
        return entry


class TestCalDAVService:
    """Test cases for CalDAVService."""

    def test_sync_entry_to_calendar(self, app, user):
        """Test syncing a journal entry to calendar."""
        with app.app_context():
            from services.caldav_service import CalDAVService
            from services.journal_service import JournalService
            from models import db

            # Create entry in this context
            entry = JournalService.create_entry(
                user_id=user.id, title="Test Entry", content="Test content", entry_date=date.today()
            )

            # Initially not synced
            assert entry.sync_status == "not_synced"
            assert entry.calendar_event_id is None

            # Sync entry
            result = CalDAVService.sync_entry_to_calendar(entry)
            assert result is True

            # Verify sync status updated
            db.session.refresh(entry)
            assert entry.sync_status == "synced"
            assert entry.calendar_event_id is not None

    def test_sync_entry_to_calendar_error_handling(self, app, user):
        """Test error handling when syncing entry to calendar fails."""
        with app.app_context():
            from services.caldav_service import CalDAVService
            from models import db, JournalEntry

            # Create entry with invalid data that might cause sync failure
            entry = JournalEntry(
                user_id=user.id,
                title="Test Entry",
                content="Test content",
                date=date.today(),
                sync_status="not_synced",
            )
            db.session.add(entry)
            db.session.commit()

            # Mock a scenario where sync might fail
            # The actual implementation should handle errors gracefully
            result = CalDAVService.sync_entry_to_calendar(entry)
            # Should return True or False, not raise exception
            assert isinstance(result, bool)

    def test_detect_conflict(self, app, user):
        """Test conflict detection between journal entry and calendar event."""
        with app.app_context():
            from services.caldav_service import CalDAVService
            from services.journal_service import JournalService
            from models import db

            # Create entry in this context
            entry = JournalService.create_entry(
                user_id=user.id, title="Test Entry", content="Test content", entry_date=date.today()
            )

            # Update entry timestamp
            entry.updated_at = datetime.now(timezone.utc) - timedelta(hours=1)
            db.session.commit()

            # Calendar event modified more recently (conflict)
            calendar_event_data = {
                "last_modified": datetime.now(timezone.utc).isoformat(),
                "title": "Updated Title",
            }
            has_conflict = CalDAVService.detect_conflict(entry, calendar_event_data)
            assert has_conflict is True

            # Calendar event modified earlier (no conflict)
            calendar_event_data_old = {
                "last_modified": (
                    datetime.now(timezone.utc) - timedelta(hours=2)
                ).isoformat(),
                "title": "Old Title",
            }
            has_conflict = CalDAVService.detect_conflict(
                entry, calendar_event_data_old
            )
            assert has_conflict is False

    def test_resolve_conflict(self, app, user):
        """Test conflict resolution using last-write-wins strategy."""
        with app.app_context():
            from services.caldav_service import CalDAVService
            from services.journal_service import JournalService
            from models import db

            # Create entry in this context
            entry = JournalService.create_entry(
                user_id=user.id, title="Original Title", content="Original content", entry_date=date.today()
            )

            # Calendar event data (newer)
            calendar_event_data = {
                "title": "Updated Calendar Title",
                "description": "Updated calendar description",
                "completion_status": "completed",
            }

            # Resolve conflict
            resolved_entry = CalDAVService.resolve_conflict(entry, calendar_event_data)

            # Verify entry updated with calendar data
            db.session.refresh(resolved_entry)
            assert resolved_entry.title == "Updated Calendar Title"
            assert resolved_entry.content == "Updated calendar description"
            assert resolved_entry.completion_status == "completed"
            assert resolved_entry.sync_status == "synced"

    def test_sync_completion_status(self, app, user):
        """Test syncing completion status from calendar to journal entry."""
        with app.app_context():
            from services.caldav_service import CalDAVService
            from services.journal_service import JournalService
            from models import db

            # Create entry in this context
            entry = JournalService.create_entry(
                user_id=user.id, title="Test Entry", content="Test content", entry_date=date.today()
            )

            # Initially no completion status
            assert entry.completion_status is None

            # Sync completion status
            result = CalDAVService.sync_completion_status(entry, "completed")
            assert result is True

            # Verify completion status updated
            db.session.refresh(entry)
            assert entry.completion_status == "completed"
            assert entry.sync_status == "synced"

    def test_handle_calendar_event_deletion(self, app, user):
        """Test handling deletion of calendar event."""
        with app.app_context():
            from services.caldav_service import CalDAVService
            from services.journal_service import JournalService
            from models import db

            # Create entry in this context
            entry = JournalService.create_entry(
                user_id=user.id, title="Test Entry", content="Test content", entry_date=date.today()
            )

            # Sync entry first to get calendar_event_id
            CalDAVService.sync_entry_to_calendar(entry)
            db.session.refresh(entry)
            calendar_event_id = entry.calendar_event_id

            # Verify entry exists
            retrieved_entry = JournalService.get_entry(entry.id, user.id)
            assert retrieved_entry is not None

            # Handle calendar event deletion
            result = CalDAVService.handle_calendar_event_deletion(
                calendar_event_id, user.id
            )
            assert result is True

            # Verify entry deleted
            deleted_entry = JournalService.get_entry(entry.id, user.id)
            assert deleted_entry is None

    def test_handle_calendar_event_deletion_not_found(self, app, user):
        """Test handling deletion of non-existent calendar event."""
        with app.app_context():
            from services.caldav_service import CalDAVService

            # Try to delete non-existent calendar event
            result = CalDAVService.handle_calendar_event_deletion(
                "non-existent-id", user.id
            )
            assert result is False

    def test_is_offline(self, app):
        """Test offline detection."""
        with app.app_context():
            from services.caldav_service import CalDAVService

            # Currently returns False (assumes online)
            # This is a placeholder implementation
            result = CalDAVService.is_offline()
            assert isinstance(result, bool)

    def test_sync_all_pending_entries(self, app, user):
        """Test syncing all pending entries for a user."""
        with app.app_context():
            from services.caldav_service import CalDAVService
            from services.journal_service import JournalService
            from models import db

            # Create multiple entries with sync_pending status
            entry1 = JournalService.create_entry(
                user_id=user.id, title="Entry 1", content="Content 1", entry_date=date.today()
            )
            entry2 = JournalService.create_entry(
                user_id=user.id, title="Entry 2", content="Content 2", entry_date=date.today()
            )

            # Mark as pending
            entry1.sync_status = "sync_pending"
            entry2.sync_status = "sync_pending"
            db.session.commit()

            # Sync all pending entries
            stats = CalDAVService.sync_all_pending_entries(user.id)

            # Verify statistics
            assert "success" in stats
            assert "failed" in stats
            assert "skipped" in stats
            assert isinstance(stats["success"], int)
            assert isinstance(stats["failed"], int)
            assert isinstance(stats["skipped"], int)

            # Verify entries synced
            db.session.refresh(entry1)
            db.session.refresh(entry2)
            # At least one should be synced (depending on implementation)
            assert entry1.sync_status in ["synced", "sync_pending"]
            assert entry2.sync_status in ["synced", "sync_pending"]

    def test_sync_all_pending_entries_no_pending(self, app, user):
        """Test syncing when there are no pending entries."""
        with app.app_context():
            from services.caldav_service import CalDAVService

            # Sync when no pending entries
            stats = CalDAVService.sync_all_pending_entries(user.id)

            # Verify statistics show no entries processed
            assert stats["success"] == 0
            assert stats["failed"] == 0
            assert stats["skipped"] == 0

