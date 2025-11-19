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
        logger.info(f"Manual calendar sync triggered by user {current_user.id}")
        result = CalDAVService.sync_all_pending_entries(current_user.id)

        logger.info(
            f"Calendar sync completed for user {current_user.id}: "
            f"success={result['success']}, failed={result['failed']}, skipped={result['skipped']}"
        )
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

    except ValueError as e:
        # Handle specific validation errors (T104)
        logger.warning(f"Calendar sync validation error for user {current_user.id}: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error syncing calendar for user {current_user.id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@caldav_bp.route("/events", methods=["GET"])
@login_required
def list_calendar_events():
    """List calendar events for the current user."""
    try:
        logger.debug(f"Listing calendar events for user {current_user.id}")
        # TODO: Implement actual calendar event listing from CalDAV server
        # For now, return empty list
        events = []
        logger.info(f"Retrieved {len(events)} calendar events for user {current_user.id}")
        return jsonify({"events": events, "total": len(events)}), 200

    except Exception as e:
        logger.error(f"Error listing calendar events for user {current_user.id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@caldav_bp.route("/events/<string:event_id>/create-entry", methods=["POST"])
@login_required
def create_entry_from_event(event_id):
    """Create a journal entry from a calendar event (FR-009)."""
    try:
        logger.info(f"Creating journal entry from calendar event {event_id} for user {current_user.id}")
        data = request.get_json() or {}

        # Extract and validate event data
        title = data.get("title", "Untitled")
        content = data.get("description", "")
        event_date = data.get("date")

        # Validate event_id
        if not event_id or not event_id.strip():
            logger.warning(f"Invalid event_id provided by user {current_user.id}")
            return jsonify({"error": "Event ID is required"}), 400

        # Create journal entry from calendar event
        entry = JournalService.create_entry_from_calendar_event(
            user_id=current_user.id,
            title=title,
            content=content,
            event_date=event_date,
            calendar_event_id=event_id,
        )

        logger.info(f"Journal entry {entry.id} created from calendar event {event_id} for user {current_user.id}")
        return jsonify(entry.to_dict()), 201

    except ValueError as e:
        # Handle specific validation errors (T104)
        logger.warning(f"Validation error creating entry from event {event_id} for user {current_user.id}: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(
            f"Error creating entry from calendar event {event_id} for user {current_user.id}: {str(e)}", exc_info=True
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
        logger.debug(f"CalDAV {method} request for path {path} by user {current_user.id}")

        if method == "PROPFIND":
            # Return calendar properties
            logger.debug(f"CalDAV PROPFIND completed for user {current_user.id}")
            return "", 207  # Multi-Status

        elif method == "GET":
            # Return calendar data
            logger.debug(f"CalDAV GET completed for user {current_user.id}")
            return "", 200

        elif method == "PUT":
            # Update calendar data
            logger.info(f"CalDAV PUT request for path {path} by user {current_user.id}")
            return "", 201  # Created

        elif method == "DELETE":
            # Delete calendar resource
            logger.info(f"CalDAV DELETE request for path {path} by user {current_user.id}")
            return "", 204  # No Content

        else:
            logger.warning(f"Unsupported CalDAV method {method} for user {current_user.id}")
            return jsonify({"error": "Method not allowed"}), 405

    except Exception as e:
        logger.error(f"Error handling CalDAV {method} request for path {path} by user {current_user.id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

