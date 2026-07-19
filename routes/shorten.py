from flask import Blueprint, request, jsonify
from models.url_model import save_url, code_exists
from utils.code_generator import generate_short_code

shorten_bp = Blueprint("shorten", __name__)


@shorten_bp.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL দিতে হবে"}), 400

    # নতুন unique short code বানানো
    short_code = generate_short_code()
    while code_exists(short_code):
        short_code = generate_short_code()

    save_url(short_code, original_url)

    short_url = request.host_url + short_code

    return jsonify({
        "short_url": short_url,
        "original_url": original_url
    }), 201