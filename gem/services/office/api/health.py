from flask import Blueprint

API = Blueprint("api_health", __name__)


@API.route("/health", methods=["GET"])
def health():
    """Returns health status of the service."""
    return "ok"
