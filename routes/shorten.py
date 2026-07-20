from flask import Blueprint, request, jsonify
from models.url_model import save_url, code_exists
from utils.code_generator import generate_short_code
import re

shorten_bp = Blueprint("shorten", __name__)


@shorten_bp.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")
    custom_alias = data.get("custom_alias", "").strip()

    if not original_url:
        return jsonify({"error": "URL দিতে হবে"}), 400

    if custom_alias:
        # শুধু letters, numbers, hyphen, underscore allow করা হবে
        if not re.match(r'^[A-Za-z0-9_-]{3,20}$', custom_alias):
            return jsonify({"error": "Custom alias শুধু 3-20 অক্ষরের letters, numbers, - বা _ হতে পারে"}), 400
        if code_exists(custom_alias):
            return jsonify({"error": "এই alias টা আগে থেকেই ব্যবহৃত হয়েছে, অন্য একটা দাও"}), 409
        short_code = custom_alias
    else:
        short_code = generate_short_code()
        while code_exists(short_code):
            short_code = generate_short_code()

    save_url(short_code, original_url)

    short_url = request.host_url + short_code

    return jsonify({
        "short_url": short_url,
        "original_url": original_url,
        "short_code": short_code
    }), 201