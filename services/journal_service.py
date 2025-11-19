"""Journal service for journal entry CRUD operations."""
import logging
from datetime import datetime, date, timezone
from typing import Optional, List, Dict
from models import db, JournalEntry

logger = logging.getLogger(__name__)


class JournalService:
    """Service for handling journal entry operations."""

    @staticmethod
    def create_entry(
        user_id: int, title: str, content: str, entry_date: Optional[date] = None
    ) -> JournalEntry:
        """
        Create a new journal entry.

        Args:
            user_id: ID of the user creating the entry
            title: Entry title (auto-generated as "Untitled" if empty per FR-029)
            content: Entry content
            entry_date: Entry date (defaults to current date if not provided)

        Returns:
            Created JournalEntry object
        """
        # Auto-generate default title if empty (FR-029)
        if not title or not title.strip():
            title = "Untitled"
            logger.info(f"Auto-generated title 'Untitled' for user {user_id}")

        # Use current date if not provided
        if entry_date is None:
            entry_date = date.today()

        entry = JournalEntry(
            user_id=user_id,
            title=title.strip(),
            content=content.strip() if content else "",
            date=entry_date,
            sync_status="not_synced",
        )

        db.session.add(entry)
        db.session.commit()

        logger.info(f"Journal entry {entry.id} created for user {user_id}")
        return entry

    @staticmethod
    def get_entry(entry_id: int, user_id: int) -> Optional[JournalEntry]:
        """
        Get a journal entry by ID for a specific user.

        Args:
            entry_id: ID of the journal entry
            user_id: ID of the user (for owner verification)

        Returns:
            JournalEntry object if found and owned by user, None otherwise
        """
        entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if entry:
            logger.debug(f"Journal entry {entry_id} retrieved for user {user_id}")
        else:
            logger.warning(f"Journal entry {entry_id} not found for user {user_id}")
        return entry

    @staticmethod
    def list_entries(
        user_id: int,
        entry_date: Optional[date] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, any]:
        """
        List journal entries for a user, optionally filtered by date.

        Args:
            user_id: ID of the user
            entry_date: Optional date filter (YYYY-MM-DD format)
            limit: Maximum number of entries to return
            offset: Number of entries to skip

        Returns:
            Dictionary with 'entries' list and 'total' count
        """
        # Use indexed columns for performance (user_id, date are indexed)
        query = JournalEntry.query.filter_by(user_id=user_id)

        if entry_date:
            query = query.filter_by(date=entry_date)

        # Optimize: count before pagination for better performance
        total = query.count()

        # Use indexed columns for ordering (date, created_at)
        entries = (
            query.order_by(JournalEntry.date.desc(), JournalEntry.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        logger.info(
            f"Retrieved {len(entries)} journal entries for user {user_id} (date: {entry_date}, total: {total})"
        )
        return {"entries": entries, "total": total}

    @staticmethod
    def update_entry(
        entry_id: int,
        user_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        entry_date: Optional[date] = None,
    ) -> Optional[JournalEntry]:
        """
        Update a journal entry.

        Args:
            entry_id: ID of the journal entry to update
            user_id: ID of the user (for owner verification)
            title: New title (optional, auto-generated as "Untitled" if empty per FR-029)
            content: New content (optional)
            entry_date: New date (optional)

        Returns:
            Updated JournalEntry object if found and updated, None otherwise
        """
        entry = JournalService.get_entry(entry_id, user_id)
        if not entry:
            return None

        if title is not None:
            # Auto-generate default title if empty (FR-029)
            if not title.strip():
                title = "Untitled"
                logger.info(f"Auto-generated title 'Untitled' for entry {entry_id}")
            entry.title = title.strip()

        if content is not None:
            entry.content = content.strip() if content else ""

        if entry_date is not None:
            entry.date = entry_date

        entry.updated_at = datetime.now(timezone.utc)

        # Mark as pending sync after update
        entry.sync_status = "sync_pending"

        db.session.commit()

        logger.info(f"Journal entry {entry_id} updated for user {user_id}")
        return entry

    @staticmethod
    def delete_entry(entry_id: int, user_id: int) -> bool:
        """
        Delete a journal entry.

        Args:
            entry_id: ID of the journal entry to delete
            user_id: ID of the user (for owner verification)

        Returns:
            True if entry was found and deleted, False otherwise
        """
        entry = JournalService.get_entry(entry_id, user_id)
        if not entry:
            return False

        db.session.delete(entry)
        db.session.commit()

        logger.info(f"Journal entry {entry_id} deleted for user {user_id}")
        return True

    @staticmethod
    def create_entry_from_calendar_event(
        user_id: int,
        title: str,
        content: str,
        event_date: Optional[date] = None,
        calendar_event_id: Optional[str] = None,
    ) -> JournalEntry:
        """
        Create a journal entry from a calendar event (FR-009).

        Args:
            user_id: ID of the user
            title: Entry title
            content: Entry content
            event_date: Entry date
            calendar_event_id: Calendar event ID

        Returns:
            Created JournalEntry object
        """
        # Auto-generate default title if empty (FR-029)
        if not title or not title.strip():
            title = "Untitled"
            logger.info(
                f"Auto-generated title 'Untitled' for calendar event {calendar_event_id}"
            )

        # Use current date if not provided
        if event_date is None:
            event_date = date.today()

        entry = JournalEntry(
            user_id=user_id,
            title=title.strip(),
            content=content.strip() if content else "",
            date=event_date,
            calendar_event_id=calendar_event_id,
            sync_status="synced",  # Already synced since it came from calendar
        )

        db.session.add(entry)
        db.session.commit()

        logger.info(
            f"Journal entry {entry.id} created from calendar event {calendar_event_id} for user {user_id}"
        )
        return entry
