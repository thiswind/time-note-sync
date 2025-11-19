"""Input validation utilities for security."""
import re
from typing import Optional


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


# Maximum lengths for input fields
MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 10000
MAX_USERNAME_LENGTH = 50


def validate_title(title: Optional[str]) -> str:
    """
    Validate and sanitize journal entry title.

    Args:
        title: Title string to validate

    Returns:
        Sanitized title string

    Raises:
        ValidationError: If title is invalid
    """
    if title is None:
        return ""

    # Strip whitespace
    title = title.strip()

    # Check length
    if len(title) > MAX_TITLE_LENGTH:
        raise ValidationError(f"Title must be {MAX_TITLE_LENGTH} characters or less")

    return title


def validate_content(content: Optional[str]) -> str:
    """
    Validate and sanitize journal entry content.

    Args:
        content: Content string to validate

    Returns:
        Sanitized content string

    Raises:
        ValidationError: If content is invalid
    """
    if content is None:
        raise ValidationError("Content is required")

    # Strip whitespace
    content = content.strip()

    # Check if empty after stripping
    if not content:
        raise ValidationError("Content cannot be empty")

    # Check length
    if len(content) > MAX_CONTENT_LENGTH:
        raise ValidationError(
            f"Content must be {MAX_CONTENT_LENGTH} characters or less"
        )

    return content


def validate_username(username: Optional[str]) -> str:
    """
    Validate username.

    Args:
        username: Username string to validate

    Returns:
        Validated username string

    Raises:
        ValidationError: If username is invalid
    """
    if not username:
        raise ValidationError("Username is required")

    username = username.strip()

    if len(username) > MAX_USERNAME_LENGTH:
        raise ValidationError(
            f"Username must be {MAX_USERNAME_LENGTH} characters or less"
        )

    # Allow alphanumeric, underscore, hyphen
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        raise ValidationError(
            "Username can only contain letters, numbers, underscores, and hyphens"
        )

    return username


def validate_date_string(date_str: Optional[str]) -> Optional[str]:
    """
    Validate date string format (YYYY-MM-DD).

    Args:
        date_str: Date string to validate

    Returns:
        Validated date string or None

    Raises:
        ValidationError: If date format is invalid
    """
    if not date_str:
        return None

    date_str = date_str.strip()

    # Check format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        raise ValidationError("Date must be in YYYY-MM-DD format")

    return date_str


def sanitize_for_display(text: str) -> str:
    """
    Sanitize text for safe display (prevent XSS).

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    # Basic HTML escaping (Vue.js will handle this, but this is a safety measure)
    # In production, use a proper HTML escaping library
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&#x27;")
    return text

