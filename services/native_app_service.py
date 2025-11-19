"""Native app service for generating URL schemes to open iPhone native apps."""
import logging
from typing import Optional
from urllib.parse import quote
from models import JournalEntry

logger = logging.getLogger(__name__)


class NativeAppService:
    """Service for generating URL schemes to open iPhone native apps."""

    @staticmethod
    def generate_calendar_url(
        entry: Optional[JournalEntry] = None, date: Optional[str] = None
    ) -> str:
        """
        Generate Calendar URL scheme (calshow://) to open iPhone Calendar.

        Args:
            entry: JournalEntry (optional, for date extraction)
            date: Date string in YYYY-MM-DD format (optional)

        Returns:
            Calendar URL scheme string
        """
        # Extract date from entry or use provided date
        target_date = None
        if entry and entry.date:
            target_date = entry.date.isoformat()
        elif date:
            target_date = date

        if target_date:
            # calshow://date format: calshow://YYYYMMDD
            date_str = target_date.replace("-", "")
            url = f"calshow://{date_str}"
        else:
            # Open calendar to current date
            url = "calshow://"

        logger.debug(f"Generated calendar URL: {url}")
        return url

    @staticmethod
    def generate_notes_url(entry: Optional[JournalEntry] = None) -> str:
        """
        Generate Notes URL scheme (mobilenotes://) to open iPhone Notes.

        Args:
            entry: JournalEntry (optional, for note identification)

        Returns:
            Notes URL scheme string
        """
        # mobilenotes:// doesn't support deep linking to specific notes
        # So we just open the Notes app
        url = "mobilenotes://"

        logger.debug(f"Generated notes URL: {url}")
        return url

