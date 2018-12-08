from flask import Blueprint

API = Blueprint("api_health", __name__)


@API.route("/health", methods=["GET"])
def index():
    """Returns health status of the service."""
    return "ok"
