from flask import Blueprint

API = Blueprint('api_health', __name__)


@API.route("/api/health", methods=["GET"])
def api_health_index():
    """Returns health status of the service."""
    return 'ok'
