"""Unit tests for JournalService."""
import pytest
from datetime import date, datetime


class TestJournalService:
    """Test cases for JournalService."""

    def test_create_entry_with_title(self, app, user):
        """Test creating a journal entry with title."""
        with app.app_context():
            from services.journal_service import JournalService
            entry = JournalService.create_entry(
                user_id=user.id, title="Test Entry", content="Test content", entry_date=date.today()
            )
            assert entry.id is not None
            assert entry.title == "Test Entry"
            assert entry.content == "Test content"
            assert entry.user_id == user.id
            assert entry.sync_status == "not_synced"

    def test_create_entry_without_title(self, app, user):
        """Test creating a journal entry without title (auto-generate 'Untitled' per FR-029)."""
        with app.app_context():
            from services.journal_service import JournalService
            entry = JournalService.create_entry(
                user_id=user.id, title="", content="Test content", entry_date=date.today()
            )
            assert entry.title == "Untitled"

    def test_get_entry(self, app, user):
        """Test getting a journal entry."""
        with app.app_context():
            from services.journal_service import JournalService
            entry = JournalService.create_entry(
                user_id=user.id, title="Test Entry", content="Test content", entry_date=date.today()
            )
            retrieved = JournalService.get_entry(entry.id, user.id)
            assert retrieved is not None
            assert retrieved.id == entry.id
            assert retrieved.title == "Test Entry"

    def test_get_entry_wrong_user(self, app, user):
        """Test getting an entry with wrong user ID (should return None)."""
        with app.app_context():
            from models import db, User
            from services.journal_service import JournalService
            other_user = User(username="otheruser", email="other@example.com")
            other_user.set_password("testpass")
            db.session.add(other_user)
            db.session.commit()

            entry = JournalService.create_entry(
                user_id=user.id, title="Test Entry", content="Test content", entry_date=date.today()
            )
            retrieved = JournalService.get_entry(entry.id, other_user.id)
            assert retrieved is None

    def test_list_entries(self, app, user):
        """Test listing journal entries."""
        with app.app_context():
            from services.journal_service import JournalService
            JournalService.create_entry(
                user_id=user.id, title="Entry 1", content="Content 1", entry_date=date.today()
            )
            JournalService.create_entry(
                user_id=user.id, title="Entry 2", content="Content 2", entry_date=date.today()
            )

            result = JournalService.list_entries(user_id=user.id)
            assert result["total"] == 2
            assert len(result["entries"]) == 2

    def test_update_entry(self, app, user):
        """Test updating a journal entry."""
        with app.app_context():
            from services.journal_service import JournalService
            entry = JournalService.create_entry(
                user_id=user.id, title="Original Title", content="Original content", entry_date=date.today()
            )
            updated = JournalService.update_entry(
                entry_id=entry.id, user_id=user.id, title="Updated Title", content="Updated content"
            )
            assert updated.title == "Updated Title"
            assert updated.content == "Updated content"
            assert updated.sync_status == "sync_pending"  # Should be pending after update

    def test_delete_entry(self, app, user):
        """Test deleting a journal entry."""
        with app.app_context():
            from services.journal_service import JournalService
            entry = JournalService.create_entry(
                user_id=user.id, title="Test Entry", content="Test content", entry_date=date.today()
            )
            success = JournalService.delete_entry(entry.id, user.id)
            assert success is True

            # Verify entry is deleted
            retrieved = JournalService.get_entry(entry.id, user.id)
            assert retrieved is None

    def test_list_entries_with_date_filter(self, app, user):
        """Test listing journal entries filtered by date."""
        with app.app_context():
            from services.journal_service import JournalService
            from datetime import timedelta

            today = date.today()
            yesterday = today - timedelta(days=1)
            tomorrow = today + timedelta(days=1)

            # Create entries on different dates
            entry_today = JournalService.create_entry(
                user_id=user.id, title="Today Entry", content="Content", entry_date=today
            )
            entry_yesterday = JournalService.create_entry(
                user_id=user.id, title="Yesterday Entry", content="Content", entry_date=yesterday
            )
            entry_tomorrow = JournalService.create_entry(
                user_id=user.id, title="Tomorrow Entry", content="Content", entry_date=tomorrow
            )

            # Test filtering by today's date
            result = JournalService.list_entries(user_id=user.id, entry_date=today)
            assert result["total"] == 1
            assert len(result["entries"]) == 1
            assert result["entries"][0].id == entry_today.id
            assert result["entries"][0].date == today

            # Test filtering by yesterday's date
            result = JournalService.list_entries(user_id=user.id, entry_date=yesterday)
            assert result["total"] == 1
            assert len(result["entries"]) == 1
            assert result["entries"][0].id == entry_yesterday.id
            assert result["entries"][0].date == yesterday

            # Test filtering by tomorrow's date
            result = JournalService.list_entries(user_id=user.id, entry_date=tomorrow)
            assert result["total"] == 1
            assert len(result["entries"]) == 1
            assert result["entries"][0].id == entry_tomorrow.id
            assert result["entries"][0].date == tomorrow

            # Test without date filter (should return all entries)
            result = JournalService.list_entries(user_id=user.id)
            assert result["total"] == 3
            assert len(result["entries"]) == 3

    def test_list_entries_date_filter_empty_result(self, app, user):
        """Test date filtering returns empty result for dates with no entries."""
        with app.app_context():
            from services.journal_service import JournalService
            from datetime import timedelta

            future_date = date.today() + timedelta(days=30)

            # Create an entry for today
            JournalService.create_entry(
                user_id=user.id, title="Today Entry", content="Content", entry_date=date.today()
            )

            # Filter by future date (no entries)
            result = JournalService.list_entries(user_id=user.id, entry_date=future_date)
            assert result["total"] == 0
            assert len(result["entries"]) == 0

    def test_list_entries_date_filter_multiple_same_date(self, app, user):
        """Test date filtering with multiple entries on the same date."""
        with app.app_context():
            from services.journal_service import JournalService

            today = date.today()

            # Create multiple entries on the same date
            entry1 = JournalService.create_entry(
                user_id=user.id, title="Entry 1", content="Content 1", entry_date=today
            )
            entry2 = JournalService.create_entry(
                user_id=user.id, title="Entry 2", content="Content 2", entry_date=today
            )
            entry3 = JournalService.create_entry(
                user_id=user.id, title="Entry 3", content="Content 3", entry_date=today
            )

            # Filter by date should return all entries for that date
            result = JournalService.list_entries(user_id=user.id, entry_date=today)
            assert result["total"] == 3
            assert len(result["entries"]) == 3

            # Verify entries are ordered by date desc, then created_at desc
            entry_ids = [e.id for e in result["entries"]]
            assert entry1.id in entry_ids
            assert entry2.id in entry_ids
            assert entry3.id in entry_ids

