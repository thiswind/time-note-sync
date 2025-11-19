"""Journal API routes for journal entry CRUD operations."""
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.journal_service import JournalService
from models import db
from utils.validation import (
    validate_title,
    validate_content,
    validate_date_string,
    ValidationError,
)

logger = logging.getLogger(__name__)

journal_bp = Blueprint("journal", __name__, url_prefix="/journal")


@journal_bp.route("/entries", methods=["GET"])
@login_required
def list_entries():
    """List journal entries, optionally filtered by date."""
    try:
        logger.debug(f"Listing journal entries for user {current_user.id}")
        # Parse and validate query parameters
        date_str = request.args.get("date")
        try:
            limit = int(request.args.get("limit", 50))
            offset = int(request.args.get("offset", 0))
        except (ValueError, TypeError):
            logger.warning(f"Invalid limit or offset parameter for user {current_user.id}")
            return jsonify({"error": "Invalid limit or offset parameter"}), 400

        # Validate limit (performance optimization: cap at 100) (T107)
        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)

        # Parse and validate date if provided
        entry_date = None
        if date_str:
            try:
                validated_date_str = validate_date_string(date_str)
                if validated_date_str:
                    entry_date = datetime.strptime(
                        validated_date_str, "%Y-%m-%d"
                    ).date()
            except (ValidationError, ValueError) as e:
                return (
                    jsonify(
                        {
                            "error": str(e)
                            if isinstance(e, ValidationError)
                            else "Invalid date format. Use YYYY-MM-DD"
                        }
                    ),
                    400,
                )

        # Get entries (uses indexed queries for performance - T107)
        result = JournalService.list_entries(
            user_id=current_user.id, entry_date=entry_date, limit=limit, offset=offset
        )

        logger.info(
            f"Retrieved {len(result['entries'])} journal entries for user {current_user.id} "
            f"(date={entry_date}, limit={limit}, offset={offset}, total={result['total']})"
        )
        return (
            jsonify(
                {
                    "entries": [entry.to_dict() for entry in result["entries"]],
                    "total": result["total"],
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error listing journal entries for user {current_user.id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries", methods=["POST"])
@login_required
def create_entry():
    """Create a new journal entry."""
    try:
        logger.debug(f"Creating journal entry for user {current_user.id}")
        data = request.get_json()

        if not data:
            logger.warning(f"Empty request body for journal entry creation by user {current_user.id}")
            return jsonify({"error": "Request body is required"}), 400

        # Extract and validate fields (T105)
        try:
            title = validate_title(data.get("title", ""))
            content = validate_content(data.get("content"))
            date_str = validate_date_string(data.get("date"))
        except ValidationError as e:
            logger.warning(f"Validation error creating journal entry for user {current_user.id}: {str(e)}")
            return jsonify({"error": str(e)}), 400

        # Parse date if provided
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                logger.warning(f"Invalid date format for journal entry creation by user {current_user.id}: {date_str}")
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        # Create entry
        entry = JournalService.create_entry(
            user_id=current_user.id, title=title, content=content, entry_date=entry_date
        )

        logger.info(f"Journal entry {entry.id} created successfully for user {current_user.id}")
        return jsonify(entry.to_dict()), 201

    except Exception as e:
        logger.error(f"Error creating journal entry for user {current_user.id}: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>", methods=["GET"])
@login_required
def get_entry(entry_id):
    """Get a specific journal entry."""
    try:
        logger.debug(f"Getting journal entry {entry_id} for user {current_user.id}")
        entry = JournalService.get_entry(entry_id, current_user.id)

        if not entry:
            logger.warning(f"Journal entry {entry_id} not found for user {current_user.id}")
            return jsonify({"error": "Journal entry not found"}), 404

        logger.debug(f"Journal entry {entry_id} retrieved successfully for user {current_user.id}")
        return jsonify(entry.to_dict()), 200

    except Exception as e:
        logger.error(f"Error getting journal entry {entry_id} for user {current_user.id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>", methods=["PUT"])
@login_required
def update_entry(entry_id):
    """Update a journal entry."""
    try:
        logger.debug(f"Updating journal entry {entry_id} for user {current_user.id}")
        data = request.get_json()

        if not data:
            logger.warning(f"Empty request body for journal entry update {entry_id} by user {current_user.id}")
            return jsonify({"error": "Request body is required"}), 400

        # Extract and validate fields (all optional for update) (T105)
        title = None
        content = None
        date_str = None

        if "title" in data:
            try:
                title = validate_title(data.get("title"))
            except ValidationError as e:
                logger.warning(f"Title validation error for entry {entry_id} by user {current_user.id}: {str(e)}")
                return jsonify({"error": str(e)}), 400

        if "content" in data:
            try:
                content = validate_content(data.get("content"))
            except ValidationError as e:
                logger.warning(f"Content validation error for entry {entry_id} by user {current_user.id}: {str(e)}")
                return jsonify({"error": str(e)}), 400

        if "date" in data:
            try:
                date_str = validate_date_string(data.get("date"))
            except ValidationError as e:
                return jsonify({"error": str(e)}), 400

        # Parse date if provided
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        # Update entry
        entry = JournalService.update_entry(
            entry_id=entry_id,
            user_id=current_user.id,
            title=title,
            content=content,
            entry_date=entry_date,
        )

        if not entry:
            return jsonify({"error": "Journal entry not found"}), 404

        return jsonify(entry.to_dict()), 200

    except Exception as e:
        logger.error(
            f"Error updating journal entry {entry_id}: {str(e)}", exc_info=True
        )
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>", methods=["DELETE"])
@login_required
def delete_entry(entry_id):
    """Delete a journal entry."""
    try:
        logger.info(f"Deleting journal entry {entry_id} for user {current_user.id}")
        success = JournalService.delete_entry(entry_id, current_user.id)

        if not success:
            logger.warning(f"Journal entry {entry_id} not found for user {current_user.id}")
            return jsonify({"error": "Journal entry not found"}), 404

        logger.info(f"Journal entry {entry_id} deleted successfully for user {current_user.id}")
        return "", 204

    except Exception as e:
        logger.error(
            f"Error deleting journal entry {entry_id} for user {current_user.id}: {str(e)}", exc_info=True
        )
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>/sync", methods=["POST"])
@login_required
def sync_entry(entry_id):
    """Sync a journal entry to calendar."""
    try:
        logger.info(f"Syncing journal entry {entry_id} to calendar for user {current_user.id}")
        entry = JournalService.get_entry(entry_id, current_user.id)

        if not entry:
            logger.warning(f"Journal entry {entry_id} not found for sync by user {current_user.id}")
            return jsonify({"error": "Journal entry not found"}), 404

        from services.caldav_service import CalDAVService

        success = CalDAVService.sync_entry_to_calendar(entry)

        if success:
            logger.info(f"Journal entry {entry_id} synced successfully to calendar for user {current_user.id}")
            return (
                jsonify(
                    {"message": "Entry synced successfully", "entry": entry.to_dict()}
                ),
                200,
            )
        else:
            logger.warning(f"Failed to sync journal entry {entry_id} to calendar for user {current_user.id}")
            return jsonify({"error": "Failed to sync entry"}), 500

    except ValueError as e:
        # Handle specific sync errors (T104)
        logger.warning(f"Sync validation error for entry {entry_id} by user {current_user.id}: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error syncing journal entry {entry_id} for user {current_user.id}: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>/export", methods=["POST"])
@login_required
def export_entry(entry_id):
    """Export a journal entry to iPhone Notes."""
    try:
        logger.info(f"Exporting journal entry {entry_id} to Notes for user {current_user.id}")
        entry = JournalService.get_entry(entry_id, current_user.id)

        if not entry:
            logger.warning(f"Journal entry {entry_id} not found for export by user {current_user.id}")
            return jsonify({"error": "Journal entry not found"}), 404

        from services.export_service import ExportService

        shortcuts_url = ExportService.export_single_entry(entry)

        logger.info(f"Journal entry {entry_id} exported successfully to Notes for user {current_user.id}")
        return jsonify({"shortcuts_url": shortcuts_url}), 200

    except ValueError as e:
        # Handle specific export errors (T093, T104)
        logger.warning(f"Export validation error for entry {entry_id} by user {current_user.id}: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(
            f"Error exporting journal entry {entry_id} for user {current_user.id}: {str(e)}", exc_info=True
        )
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/batch-export", methods=["POST"])
@login_required
def batch_export_entries():
    """Export multiple journal entries to iPhone Notes."""
    try:
        logger.info(f"Batch exporting journal entries to Notes for user {current_user.id}")
        data = request.get_json()
        if not data:
            logger.warning(f"Empty request body for batch export by user {current_user.id}")
            return jsonify({"error": "Request body is required"}), 400

        entry_ids = data.get("entry_ids", [])
        if not entry_ids:
            logger.warning(f"Empty entry_ids for batch export by user {current_user.id}")
            return jsonify({"error": "entry_ids is required"}), 400

        # Get entries
        entries = []
        for entry_id in entry_ids:
            entry = JournalService.get_entry(entry_id, current_user.id)
            if entry:
                entries.append(entry)

        if not entries:
            logger.warning(f"No valid entries found for batch export by user {current_user.id}")
            return jsonify({"error": "No valid entries found"}), 404

        from services.export_service import ExportService

        shortcuts_url = ExportService.export_multiple_entries(entries)

        logger.info(f"Batch exported {len(entries)} journal entries to Notes for user {current_user.id}")
        return jsonify({"shortcuts_url": shortcuts_url}), 200

    except ValueError as e:
        # Handle specific export errors (T093, T104)
        logger.warning(f"Batch export validation error for user {current_user.id}: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error batch exporting entries for user {current_user.id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>/open-calendar", methods=["GET"])
@login_required
def open_calendar(entry_id):
    """Get Calendar URL scheme for opening iPhone Calendar with entry date."""
    try:
        logger.debug(f"Generating calendar URL for entry {entry_id} for user {current_user.id}")
        entry = JournalService.get_entry(entry_id, current_user.id)

        if not entry:
            logger.warning(f"Journal entry {entry_id} not found for calendar URL by user {current_user.id}")
            return jsonify({"error": "Journal entry not found"}), 404

        from services.native_app_service import NativeAppService

        calendar_url = NativeAppService.generate_calendar_url(entry=entry)

        logger.info(f"Generated calendar URL for entry {entry_id} for user {current_user.id}")
        return jsonify({"calendar_url": calendar_url}), 200

    except Exception as e:
        logger.error(
            f"Error generating calendar URL for entry {entry_id} for user {current_user.id}: {str(e)}", exc_info=True
        )
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>/open-notes", methods=["GET"])
@login_required
def open_notes(entry_id):
    """Get Notes URL scheme for opening iPhone Notes."""
    try:
        logger.debug(f"Generating notes URL for entry {entry_id} for user {current_user.id}")
        entry = JournalService.get_entry(entry_id, current_user.id)

        if not entry:
            logger.warning(f"Journal entry {entry_id} not found for notes URL by user {current_user.id}")
            return jsonify({"error": "Journal entry not found"}), 404

        from services.native_app_service import NativeAppService

        notes_url = NativeAppService.generate_notes_url(entry=entry)

        logger.info(f"Generated notes URL for entry {entry_id} for user {current_user.id}")
        return jsonify({"notes_url": notes_url}), 200

    except Exception as e:
        logger.error(
            f"Error generating notes URL for entry {entry_id} for user {current_user.id}: {str(e)}", exc_info=True
        )
        return jsonify({"error": "Internal server error"}), 500
