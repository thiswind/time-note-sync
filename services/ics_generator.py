"""iCalendar generator service for converting journal entries to .ics format."""
import logging
from datetime import datetime, date, timedelta, timezone
from typing import Optional
from ics import Calendar, Event
from models.journal_entry import JournalEntry

logger = logging.getLogger(__name__)


class ICSGenerator:
    """Service for generating iCalendar (.ics) files from journal entries."""

    # Maximum length for calendar event title (FR-026)
    MAX_TITLE_LENGTH = 100
    # Maximum length for calendar event description (FR-026)
    MAX_DESCRIPTION_LENGTH = 500

    @staticmethod
    def truncate_text(text: str, max_length: int, ellipsis: str = "...") -> str:
        """
        Truncate text to maximum length with ellipsis.

        Args:
            text: Text to truncate
            max_length: Maximum length
            ellipsis: Ellipsis string to append

        Returns:
            Truncated text
        """
        if not text:
            return ""
        if len(text) <= max_length:
            return text
        return text[: max_length - len(ellipsis)] + ellipsis

    @staticmethod
    def strip_formatting(text: str) -> str:
        """
        Strip formatting from text, preserving content (FR-027).

        Args:
            text: Text with potential formatting

        Returns:
            Plain text without formatting
        """
        if not text:
            return ""
        # Remove HTML tags if present
        import re

        text = re.sub(r"<[^>]+>", "", text)
        # Remove markdown formatting
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)  # Bold
        text = re.sub(r"\*([^*]+)\*", r"\1", text)  # Italic
        text = re.sub(r"`([^`]+)`", r"\1", text)  # Code
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # Links
        # Preserve emoji and special characters
        return text.strip()

    @staticmethod
    def generate_event_from_entry(
        entry: JournalEntry, time_offset_minutes: int = 0
    ) -> Event:
        """
        Generate an iCalendar Event from a JournalEntry.

        Args:
            entry: JournalEntry to convert
            time_offset_minutes: Time offset in minutes for multiple entries on same date/time (FR-028)

        Returns:
            iCalendar Event object
        """
        # Prepare title (truncate if needed, FR-026)
        title = ICSGenerator.strip_formatting(entry.title or "Untitled")
        title = ICSGenerator.truncate_text(title, ICSGenerator.MAX_TITLE_LENGTH)

        # Prepare description (truncate if needed, FR-026)
        # Preserve text content including emoji and special characters (FR-027)
        description = ICSGenerator.strip_formatting(entry.content or "")
        description = ICSGenerator.truncate_text(
            description, ICSGenerator.MAX_DESCRIPTION_LENGTH
        )

        # Convert date to datetime (use UTC, FR-025)
        entry_date = entry.date
        if isinstance(entry_date, date):
            # Default to 9:00 AM UTC, add offset for multiple entries
            start_datetime = datetime.combine(
                entry_date, datetime.min.time().replace(hour=9)
            )
            start_datetime = start_datetime + timedelta(minutes=time_offset_minutes)
        else:
            start_datetime = datetime.now(timezone.utc)

        # End time is 1 hour after start
        end_datetime = start_datetime + timedelta(hours=1)

        # Create event
        event = Event()
        event.name = title
        event.description = description
        event.begin = start_datetime
        event.end = end_datetime
        event.uid = f"journal-entry-{entry.id}@{entry.user_id}"

        # Add metadata - skip for now as ics 0.7.x Container API is complex
        # Metadata can be added via description or custom properties if needed
        # For now, entry ID is in the UID which is sufficient for identification

        logger.debug(f"Generated iCalendar event for journal entry {entry.id}")
        return event

    @staticmethod
    def generate_calendar_from_entries(entries: list[JournalEntry]) -> Calendar:
        """
        Generate an iCalendar Calendar from a list of JournalEntries.

        Args:
            entries: List of JournalEntry objects

        Returns:
            iCalendar Calendar object
        """
        calendar = Calendar()

        # Group entries by date and time to handle multiple entries on same date/time (FR-028)
        entries_by_datetime = {}
        for entry in entries:
            entry_key = (
                entry.date.isoformat()
                if isinstance(entry.date, date)
                else str(entry.date)
            )
            if entry_key not in entries_by_datetime:
                entries_by_datetime[entry_key] = []
            entries_by_datetime[entry_key].append(entry)

        # Generate events with time offsets for multiple entries on same date
        for entry_key, entry_list in entries_by_datetime.items():
            for index, entry in enumerate(entry_list):
                time_offset = index * 30  # 30 minutes offset per entry
                event = ICSGenerator.generate_event_from_entry(entry, time_offset)
                calendar.events.add(event)

        logger.info(f"Generated iCalendar calendar with {len(calendar.events)} events")
        return calendar

    @staticmethod
    def generate_ics_string(entries: list[JournalEntry]) -> str:
        """
        Generate an iCalendar (.ics) string from journal entries.

        Args:
            entries: List of JournalEntry objects

        Returns:
            iCalendar string
        """
        calendar = ICSGenerator.generate_calendar_from_entries(entries)
        # Use str() for ics 0.7.x compatibility
        return str(calendar)
