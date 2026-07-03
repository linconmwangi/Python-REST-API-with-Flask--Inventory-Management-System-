"""
Flask Application Factory
Initializes and configures the Flask application
"""

from flask import Flask
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)


def create_app(config=None):
    """
    Create and configure Flask application
    
    Args:
        config (dict): Optional configuration dictionary
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Apply configuration
    if config:
        app.config.update(config)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api)
    
    # Health check route
    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "healthy", "service": "Inventory Management API"}, 200
    
    # 404 error handler
    @app.errorhandler(404)
    def not_found(error):
        return {
            "status": "error",
            "message": "Resource not found"
        }, 404
    
    # 500 error handler
    @app.errorhandler(500)
    def server_error(error):
        return {
            "status": "error",
            "message": "Internal server error"
        }, 500
    
    return app
