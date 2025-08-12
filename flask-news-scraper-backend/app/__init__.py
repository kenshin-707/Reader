from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from app.utils.logging_config import configure_logging
from app.routes.news_routes import news_bp

def create_app():
    app = Flask(__name__)

    # Configure logging
    configure_logging()

    # Rate limiting (100 requests/day per IP)
    limiter = Limiter(get_remote_address, app=app, default_limits=["100/day"])

    # Register Blueprints
    app.register_blueprint(news_bp, url_prefix="/api")

    return app
