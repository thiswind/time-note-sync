"""API routes package."""
from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Import routes to register them
from . import journal_routes
from . import auth_routes
from . import caldav_routes

# Register blueprints
api_bp.register_blueprint(journal_routes.journal_bp)
api_bp.register_blueprint(auth_routes.auth_bp)
api_bp.register_blueprint(caldav_routes.caldav_bp)
