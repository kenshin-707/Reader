from flask import Blueprint, request, jsonify
from app.utils.validation import validate_site, sanitize_keyword
from app.services.scraper_service import scrape_articles
import logging

news_bp = Blueprint("news", __name__)
logger = logging.getLogger(__name__)

@news_bp.route("/scrape", methods=["GET"])
def scrape():
    try:
        site = request.args.get("site", "").strip()
        keyword = request.args.get("keyword", "").strip()

        if not validate_site(site):
            return jsonify({"error": "Invalid site selection"}), 400

        keyword = sanitize_keyword(keyword)
        if not keyword:
            return jsonify({"error": "Invalid keyword"}), 400

        articles = scrape_articles(site, keyword)
        return jsonify({"articles": articles})

    except Exception as e:
        logger.exception("Error during scraping")
        return jsonify({"error": "Internal Server Error"}), 500
