"""Flask application entry point."""
import logging
import os
from flask import Flask, jsonify, render_template
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
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Load configuration
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from api import api_bp

    app.register_blueprint(api_bp)

    # Register template routes
    @app.route("/")
    @app.route("/home")
    def home():
        """Home page route."""
        from flask_login import current_user
        if not current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for("login"))
        return render_template("index.html")

    @app.route("/login")
    def login():
        """Login page route."""
        from flask_login import current_user
        if current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for("home"))
        return render_template("login.html")

    @app.route("/entry/new")
    def entry_new():
        """New entry page route."""
        from flask_login import current_user
        if not current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for("login"))
        return render_template("entry_detail.html", entry_id=None)

    @app.route("/entry/<int:entry_id>")
    def entry_detail(entry_id):
        """Entry detail page route."""
        from flask_login import current_user, login_required
        from flask import abort
        if not current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for("login"))
        return render_template("entry_detail.html", entry_id=entry_id)

    @app.route("/settings")
    def settings():
        """Settings page route."""
        from flask_login import current_user, login_required
        if not current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for("login"))
        return render_template("settings.html")

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


# Create app instance for Vercel serverless function
# Vercel Python runtime requires 'app' to be available at module level
config_name = os.environ.get("FLASK_ENV", "production")
app = create_app(config_name)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
