"""Integration tests for CalDAV calendar synchronization."""
import pytest
from datetime import date
from services.journal_service import JournalService
from services.caldav_service import CalDAVService


class TestCalDAVSync:
    """Integration tests for calendar synchronization."""

    def test_sync_entry_to_calendar(self, app, user):
        """Test syncing a journal entry to calendar."""
        with app.app_context():
            from services.journal_service import JournalService
            from services.caldav_service import CalDAVService

            # Create a journal entry
            entry = JournalService.create_entry(
                user_id=user.id,
                title="Test Sync Entry",
                content="This is a test entry for sync",
                entry_date=date.today(),
            )

            # Sync to calendar (this will be a placeholder in MVP)
            # In full implementation, this would actually sync to CalDAV server
            result = CalDAVService.sync_entry_to_calendar(entry)

            # For MVP, we just verify the method exists and doesn't crash
            # Full sync implementation will be tested with actual CalDAV server
            assert result is not None

    def test_sync_all_pending_entries(self, app, user):
        """Test syncing all pending entries."""
        with app.app_context():
            from services.journal_service import JournalService
            from services.caldav_service import CalDAVService

            # Create multiple entries
            entry1 = JournalService.create_entry(
                user_id=user.id,
                title="Entry 1",
                content="Content 1",
                entry_date=date.today(),
            )
            entry2 = JournalService.create_entry(
                user_id=user.id,
                title="Entry 2",
                content="Content 2",
                entry_date=date.today(),
            )

            # Sync all pending entries
            result = CalDAVService.sync_all_pending_entries(user.id)

            # Verify result structure
            assert "success" in result
            assert "failed" in result
            assert "skipped" in result





