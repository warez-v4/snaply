from flask import Blueprint, jsonify
from models.url_model import get_stats

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/api/stats/<short_code>")
def link_stats(short_code):
    stats = get_stats(short_code)
    if stats is None:
        return jsonify({"error": "লিংকটা পাওয়া যায়নি (হয়তো 3 মিনিট পার হয়ে গেছে)"}), 404
    return jsonify(stats), 200