from flask import Blueprint, jsonify, request
from reports.proposals import proposal_artifacts_report

from utils import print_and_save

API_PROPOSAL = Blueprint("api_proposal", __name__)


@API_PROPOSAL.route("/proposals/artifacts", methods=["GET"])
def generate_proposal_artifacts_report():
    """Generates proposal report."""
    proposal_id = request.args.get("proposal")
    report = proposal_artifacts_report(proposal_id=proposal_id)
    filename = print_and_save(report)
    return jsonify({"success": True, "filename": filename})
