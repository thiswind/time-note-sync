"""Flask application entry point."""
import logging
import os
from flask import Flask, jsonify
from flask_login import LoginManager
from config import config
from models import db, User

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Flask extensions
login_manager = LoginManager()
login_manager.login_view = "api.auth.login"
login_manager.session_protection = "strong"


@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access for API requests."""
    from flask import jsonify

    return jsonify({"error": "Authentication required"}), 401


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))


def create_app(config_name=None):
    """
    Create and configure the Flask application.

    Args:
        config_name: Configuration name (development, production, testing)

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from api import api_bp

    app.register_blueprint(api_bp)

    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    # Health check endpoint
    @app.route("/health")
    def health():
        """Health check endpoint for monitoring."""
        return jsonify({"status": "healthy"}), 200

    # CORS configuration for frontend (if needed)
    @app.after_request
    def after_request(response):
        """Add security headers and CORS if needed."""
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    logger.info(f"Flask application created with config: {config_name}")
    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
