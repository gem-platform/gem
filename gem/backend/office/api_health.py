from flask import Blueprint

API_HEALTH = Blueprint("api_health", __name__)


@API_HEALTH.route("/health", methods=["GET"])
def health():
    """Returns health status of the service."""
    return "ok"
