"""CalDAV API routes for calendar synchronization."""
import logging
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.caldav_service import CalDAVService
from services.journal_service import JournalService
from models import db

logger = logging.getLogger(__name__)

caldav_bp = Blueprint("calendar", __name__, url_prefix="/calendar")


@caldav_bp.route("/sync", methods=["POST"])
@login_required
def sync_calendar():
    """Manual sync trigger for all pending entries."""
    try:
        result = CalDAVService.sync_all_pending_entries(current_user.id)

        return (
            jsonify(
                {
                    "message": "Sync completed",
                    "success": result["success"],
                    "failed": result["failed"],
                    "skipped": result["skipped"],
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error syncing calendar: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@caldav_bp.route("/events", methods=["GET"])
@login_required
def list_calendar_events():
    """List calendar events for the current user."""
    try:
        # TODO: Implement actual calendar event listing from CalDAV server
        # For now, return empty list
        return jsonify({"events": [], "total": 0}), 200

    except Exception as e:
        logger.error(f"Error listing calendar events: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@caldav_bp.route("/events/<string:event_id>/create-entry", methods=["POST"])
@login_required
def create_entry_from_event(event_id):
    """Create a journal entry from a calendar event (FR-009)."""
    try:
        data = request.get_json() or {}

        # Extract event data
        title = data.get("title", "Untitled")
        content = data.get("description", "")
        event_date = data.get("date")

        # Create journal entry from calendar event
        entry = JournalService.create_entry_from_calendar_event(
            user_id=current_user.id,
            title=title,
            content=content,
            event_date=event_date,
            calendar_event_id=event_id,
        )

        return jsonify(entry.to_dict()), 201

    except Exception as e:
        logger.error(
            f"Error creating entry from calendar event: {str(e)}", exc_info=True
        )
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


# CalDAV protocol endpoints (PROPFIND, GET, PUT, DELETE)
@caldav_bp.route("/caldav/<path:path>", methods=["PROPFIND", "GET", "PUT", "DELETE"])
@login_required
def caldav_protocol(path):
    """Handle CalDAV protocol requests."""
    try:
        method = request.method

        if method == "PROPFIND":
            # Return calendar properties
            return "", 207  # Multi-Status

        elif method == "GET":
            # Return calendar data
            return "", 200

        elif method == "PUT":
            # Update calendar data
            return "", 201  # Created

        elif method == "DELETE":
            # Delete calendar resource
            return "", 204  # No Content

        else:
            return jsonify({"error": "Method not allowed"}), 405

    except Exception as e:
        logger.error(f"Error handling CalDAV request: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500




