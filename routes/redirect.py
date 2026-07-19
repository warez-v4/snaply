from flask import Blueprint, redirect, abort
from models.url_model import get_original_url, increment_clicks

redirect_bp = Blueprint("redirect", __name__)


@redirect_bp.route("/<short_code>")
def redirect_to_url(short_code):
    original_url = get_original_url(short_code)

    if original_url is None:
        abort(404)

    increment_clicks(short_code)
    return redirect(original_url)