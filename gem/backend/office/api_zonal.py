from flask import Blueprint, jsonify, request
from reports.za import zonal_assignments_report

from utils import print_and_save

API = Blueprint("api_zonal", __name__)


@API.route("/zonal/assignments", methods=["GET"])
def generate_zonal_report():
    hierarchy = request.args.get("hierarchy") in ["true", 1]
    leaves_only = request.args.get("leavesOnly") in ["true", 1]
    report = zonal_assignments_report(
        hierarchy=hierarchy, leaves_only=leaves_only)
    filename = print_and_save(report)
    return jsonify({"success": True, "filename": filename})
