"""Authentication API routes."""
import logging
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from services.auth_service import AuthService
from utils.validation import validate_username, ValidationError

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login endpoint."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Validate username format
        try:
            username = validate_username(username)
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

        # Basic password validation (minimum length)
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        user = AuthService.authenticate(username, password)
        if user:
            AuthService.login(user, remember=True)
            return (
                jsonify(
                    {
                        "message": "Login successful",
                        "user": {"id": user.id, "username": user.username},
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Logout endpoint."""
    try:
        AuthService.logout()
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route("/status", methods=["GET"])
def status():
    """Check authentication status."""
    try:
        if current_user.is_authenticated:
            logger.debug(f"Authentication status check: user {current_user.id} is authenticated")
            return (
                jsonify(
                    {
                        "authenticated": True,
                        "user": {"id": current_user.id, "username": current_user.username},
                    }
                ),
                200,
            )
        else:
            logger.debug("Authentication status check: user is not authenticated")
            return jsonify({"authenticated": False}), 200
    except Exception as e:
        logger.error(f"Error checking authentication status: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
