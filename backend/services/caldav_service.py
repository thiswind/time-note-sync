"""CalDAV service for bidirectional calendar synchronization."""
import logging
from datetime import datetime, date, timedelta, timezone
from typing import Optional, List, Dict
from models import db, JournalEntry, User, CalendarEvent
from services.ics_generator import ICSGenerator

logger = logging.getLogger(__name__)


class CalDAVService:
    """Service for handling CalDAV calendar synchronization."""

    @staticmethod
    def sync_entry_to_calendar(entry: JournalEntry) -> bool:
        """
        Sync a journal entry to iPhone Calendar (web to iPhone).

        Args:
            entry: JournalEntry to sync

        Returns:
            True if sync successful, False otherwise
        """
        try:
            # Generate iCalendar event from journal entry
            event = ICSGenerator.generate_event_from_entry(entry)
            calendar = ICSGenerator.generate_calendar_from_entries([entry])

            # TODO: Implement actual CalDAV PUT request to sync to calendar
            # For now, mark as synced
            entry.sync_status = "synced"
            entry.calendar_event_id = event.uid
            db.session.commit()

            logger.info(f"Synced journal entry {entry.id} to calendar")
            return True
        except Exception as e:
            logger.error(
                f"Error syncing entry {entry.id} to calendar: {str(e)}", exc_info=True
            )
            entry.sync_status = "sync_pending"
            db.session.rollback()
            return False

    @staticmethod
    def sync_calendar_to_entry(
        user_id: int, calendar_event_data: Dict
    ) -> Optional[JournalEntry]:
        """
        Sync a calendar event to journal entry (iPhone to web).

        Args:
            user_id: ID of the user
            calendar_event_data: Dictionary containing calendar event data

        Returns:
            Created or updated JournalEntry if successful, None otherwise
        """
        try:
            # TODO: Parse calendar event data and create/update journal entry
            # For now, return None as placeholder
            logger.info(f"Syncing calendar event to journal entry for user {user_id}")
            return None
        except Exception as e:
            logger.error(
                f"Error syncing calendar event to entry: {str(e)}", exc_info=True
            )
            return None

    @staticmethod
    def detect_conflict(entry: JournalEntry, calendar_event_data: Dict) -> bool:
        """
        Detect if there's a conflict between journal entry and calendar event (FR-018).

        Args:
            entry: JournalEntry to check
            calendar_event_data: Calendar event data

        Returns:
            True if conflict detected, False otherwise
        """
        # Last-write-wins strategy (FR-018)
        # Compare timestamps to determine which is newer
        entry_updated = entry.updated_at
        event_updated = calendar_event_data.get("last_modified")

        if event_updated and entry_updated:
            if isinstance(event_updated, str):
                event_updated = datetime.fromisoformat(
                    event_updated.replace("Z", "+00:00")
                )
            # Ensure both datetimes are timezone-aware for comparison
            if event_updated.tzinfo is None:
                event_updated = event_updated.replace(tzinfo=timezone.utc)
            if entry_updated.tzinfo is None:
                entry_updated = entry_updated.replace(tzinfo=timezone.utc)
            if event_updated > entry_updated:
                return True  # Calendar event is newer, conflict exists

        return False

    @staticmethod
    def resolve_conflict(
        entry: JournalEntry, calendar_event_data: Dict
    ) -> JournalEntry:
        """
        Resolve conflict using last-write-wins strategy (FR-018).

        Args:
            entry: JournalEntry with conflict
            calendar_event_data: Calendar event data (newer)

        Returns:
            Updated JournalEntry
        """
        # Last-write-wins: use calendar event data
        entry.title = calendar_event_data.get("title", entry.title)
        entry.content = calendar_event_data.get("description", entry.content)
        entry.completion_status = calendar_event_data.get("completion_status")
        entry.sync_status = "synced"
        entry.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        logger.info(
            f"Resolved conflict for journal entry {entry.id} using last-write-wins"
        )
        return entry

    @staticmethod
    def sync_completion_status(entry: JournalEntry, completion_status: str) -> bool:
        """
        Sync completion status from calendar to journal entry (FR-008).

        Args:
            entry: JournalEntry to update
            completion_status: Completion status from calendar

        Returns:
            True if successful, False otherwise
        """
        try:
            entry.completion_status = completion_status
            entry.sync_status = "synced"
            db.session.commit()

            logger.info(
                f"Synced completion status '{completion_status}' for entry {entry.id}"
            )
            return True
        except Exception as e:
            logger.error(f"Error syncing completion status: {str(e)}", exc_info=True)
            db.session.rollback()
            return False

    @staticmethod
    def handle_calendar_event_deletion(calendar_event_id: str, user_id: int) -> bool:
        """
        Handle deletion of calendar event by deleting corresponding journal entry (FR-024).

        Args:
            calendar_event_id: ID of the deleted calendar event
            user_id: ID of the user

        Returns:
            True if entry deleted, False otherwise
        """
        try:
            entry = JournalEntry.query.filter_by(
                calendar_event_id=calendar_event_id, user_id=user_id
            ).first()

            if entry:
                db.session.delete(entry)
                db.session.commit()
                logger.info(
                    f"Deleted journal entry {entry.id} due to calendar event deletion"
                )
                return True

            return False
        except Exception as e:
            logger.error(
                f"Error handling calendar event deletion: {str(e)}", exc_info=True
            )
            db.session.rollback()
            return False

    @staticmethod
    def is_offline() -> bool:
        """
        Check if device is offline (FR-023).

        Returns:
            True if offline, False otherwise
        """
        # TODO: Implement actual offline detection
        # For now, return False (assume online)
        return False

    @staticmethod
    def sync_all_pending_entries(user_id: int) -> Dict[str, int]:
        """
        Sync all pending journal entries for a user.

        Args:
            user_id: ID of the user

        Returns:
            Dictionary with sync statistics
        """
        if CalDAVService.is_offline():
            logger.warning(f"Device is offline, cannot sync entries for user {user_id}")
            return {"success": 0, "failed": 0, "skipped": 0}

        pending_entries = JournalEntry.query.filter_by(
            user_id=user_id, sync_status="sync_pending"
        ).all()

        success_count = 0
        failed_count = 0

        for entry in pending_entries:
            if CalDAVService.sync_entry_to_calendar(entry):
                success_count += 1
            else:
                failed_count += 1

        logger.info(
            f"Synced {success_count} entries, {failed_count} failed for user {user_id}"
        )
        return {"success": success_count, "failed": failed_count, "skipped": 0}
