from flask import Blueprint

api_health = Blueprint('api_health', __name__)


@api_health.route("/api/health", methods=["GET"])
def api_health_index():
    """Returns health status of the service."""
    return 'ok'
