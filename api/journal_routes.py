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
        # Parse and validate query parameters
        date_str = request.args.get("date")
        try:
            limit = int(request.args.get("limit", 50))
            offset = int(request.args.get("offset", 0))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid limit or offset parameter"}), 400

        # Validate limit (performance optimization: cap at 100)
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

        # Get entries
        result = JournalService.list_entries(
            user_id=current_user.id, entry_date=entry_date, limit=limit, offset=offset
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
        logger.error(f"Error listing journal entries: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries", methods=["POST"])
@login_required
def create_entry():
    """Create a new journal entry."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # Extract and validate fields
        try:
            title = validate_title(data.get("title", ""))
            content = validate_content(data.get("content"))
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

        # Create entry
        entry = JournalService.create_entry(
            user_id=current_user.id, title=title, content=content, entry_date=entry_date
        )

        return jsonify(entry.to_dict()), 201

    except Exception as e:
        logger.error(f"Error creating journal entry: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>", methods=["GET"])
@login_required
def get_entry(entry_id):
    """Get a specific journal entry."""
    try:
        entry = JournalService.get_entry(entry_id, current_user.id)

        if not entry:
            return jsonify({"error": "Journal entry not found"}), 404

        return jsonify(entry.to_dict()), 200

    except Exception as e:
        logger.error(f"Error getting journal entry {entry_id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>", methods=["PUT"])
@login_required
def update_entry(entry_id):
    """Update a journal entry."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # Extract and validate fields (all optional for update)
        title = None
        content = None
        date_str = None

        if "title" in data:
            try:
                title = validate_title(data.get("title"))
            except ValidationError as e:
                return jsonify({"error": str(e)}), 400

        if "content" in data:
            try:
                content = validate_content(data.get("content"))
            except ValidationError as e:
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
        success = JournalService.delete_entry(entry_id, current_user.id)

        if not success:
            return jsonify({"error": "Journal entry not found"}), 404

        return "", 204

    except Exception as e:
        logger.error(
            f"Error deleting journal entry {entry_id}: {str(e)}", exc_info=True
        )
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>/sync", methods=["POST"])
@login_required
def sync_entry(entry_id):
    """Sync a journal entry to calendar."""
    try:
        entry = JournalService.get_entry(entry_id, current_user.id)

        if not entry:
            return jsonify({"error": "Journal entry not found"}), 404

        from services.caldav_service import CalDAVService

        success = CalDAVService.sync_entry_to_calendar(entry)

        if success:
            return (
                jsonify(
                    {"message": "Entry synced successfully", "entry": entry.to_dict()}
                ),
                200,
            )
        else:
            return jsonify({"error": "Failed to sync entry"}), 500

    except Exception as e:
        logger.error(f"Error syncing journal entry {entry_id}: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/<int:entry_id>/export", methods=["POST"])
@login_required
def export_entry(entry_id):
    """Export a journal entry to iPhone Notes."""
    try:
        entry = JournalService.get_entry(entry_id, current_user.id)

        if not entry:
            return jsonify({"error": "Journal entry not found"}), 404

        from services.export_service import ExportService

        shortcuts_url = ExportService.export_single_entry(entry)

        return jsonify({"shortcuts_url": shortcuts_url}), 200

    except ValueError as e:
        # Handle specific export errors (T093)
        logger.warning(f"Export validation error for entry {entry_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(
            f"Error exporting journal entry {entry_id}: {str(e)}", exc_info=True
        )
        return jsonify({"error": "Internal server error"}), 500


@journal_bp.route("/entries/batch-export", methods=["POST"])
@login_required
def batch_export_entries():
    """Export multiple journal entries to iPhone Notes."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400

        entry_ids = data.get("entry_ids", [])
        if not entry_ids:
            return jsonify({"error": "entry_ids is required"}), 400

        # Get entries
        entries = []
        for entry_id in entry_ids:
            entry = JournalService.get_entry(entry_id, current_user.id)
            if entry:
                entries.append(entry)

        if not entries:
            return jsonify({"error": "No valid entries found"}), 404

        from services.export_service import ExportService

        shortcuts_url = ExportService.export_multiple_entries(entries)

        return jsonify({"shortcuts_url": shortcuts_url}), 200

    except ValueError as e:
        # Handle specific export errors (T093)
        logger.warning(f"Batch export validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error batch exporting entries: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
