"""Export service for exporting journal entries to iPhone Notes via Shortcuts."""
import logging
from typing import List, Optional
from urllib.parse import quote
from models import JournalEntry
from services.ics_generator import ICSGenerator

logger = logging.getLogger(__name__)


class ExportService:
    """Service for exporting journal entries to iPhone Notes."""

    # Maximum length for Notes content (FR-026)
    MAX_CONTENT_LENGTH = 10000

    @staticmethod
    def format_entry_for_notes(entry: JournalEntry) -> str:
        """
        Format a journal entry for Notes export (FR-027).

        Args:
            entry: JournalEntry to format

        Returns:
            Formatted text string
        """
        # Strip formatting, preserve text content including emoji and special characters (FR-027)
        title = ICSGenerator.strip_formatting(entry.title or "Untitled")
        content = ICSGenerator.strip_formatting(entry.content or "")

        # Truncate if needed (FR-026)
        if len(content) > ExportService.MAX_CONTENT_LENGTH:
            content = ICSGenerator.truncate_text(
                content, ExportService.MAX_CONTENT_LENGTH
            )

        # Format as simple text
        formatted = f"{title}\n\n{content}"

        # Add date if available
        if entry.date:
            formatted += f"\n\n日期: {entry.date.isoformat()}"

        return formatted

    @staticmethod
    def generate_shortcuts_url(entries: List[JournalEntry]) -> str:
        """
        Generate Shortcuts URL for exporting entries to Notes.

        Args:
            entries: List of JournalEntry objects to export

        Returns:
            Shortcuts URL string
        """
        if not entries:
            raise ValueError("No entries to export")

        # Format all entries
        formatted_entries = []
        for entry in entries:
            formatted_text = ExportService.format_entry_for_notes(entry)
            formatted_entries.append(formatted_text)

        # Combine all entries with separator
        combined_text = "\n\n---\n\n".join(formatted_entries)

        # URL encode the text
        encoded_text = quote(combined_text)

        # Generate Shortcuts URL
        # Note: This assumes a Shortcuts shortcut named "AddToNotes" exists
        # The actual implementation may vary based on Shortcuts configuration
        shortcuts_url = (
            f"shortcuts://run-shortcut?name=AddToNotes&input=text&text={encoded_text}"
        )

        logger.info(f"Generated Shortcuts URL for {len(entries)} entries")
        return shortcuts_url

    @staticmethod
    def export_single_entry(entry: JournalEntry) -> str:
        """
        Export a single journal entry to Notes.

        Args:
            entry: JournalEntry to export

        Returns:
            Shortcuts URL
        """
        return ExportService.generate_shortcuts_url([entry])

    @staticmethod
    def export_multiple_entries(entries: List[JournalEntry]) -> str:
        """
        Export multiple journal entries to Notes.

        Args:
            entries: List of JournalEntry objects to export

        Returns:
            Shortcuts URL
        """
        if not entries:
            raise ValueError("No entries to export")

        return ExportService.generate_shortcuts_url(entries)




