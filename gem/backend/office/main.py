from os import environ
from io import BytesIO
from uuid import uuid4
from requests import post
from flask import Flask, jsonify, request

from gem.utils.db import connect_db

from reports.za import zonal_assignments_report
from reports.proposals import proposal_comments_report

connect_db()
app = Flask("office")


def print_and_save(content):
    stream = BytesIO(content.encode())
    files = {"file": stream}
    req = post("http://pdf-printer:4999/pdf", files=files)
    filename = str(uuid4()) + ".pdf"
    w = open("/usr/shared/downloads/" + filename, "wb")
    w.write(req.content)
    w.close()
    return filename


@app.route("/office/health", methods=["GET"])
def generate_health():
    """Returns health status of the service."""
    return 'ok'


@app.route("/office/zonal/report", methods=["GET"])
def generate_zonal_report():
    hierarchy = request.args.get("hierarchy") in ["true", 1]
    leaves_only = request.args.get("leavesOnly") in ["true", 1]
    report = zonal_assignments_report(
        hierarchy=hierarchy, leaves_only=leaves_only)
    filename = print_and_save(report)
    return jsonify({"success": True, "filename": filename})


@app.route("/office/proposals/comments", methods=["GET"])
def generate_proposal_comments_report():
    proposal_id = request.args.get("proposal")

    report = proposal_comments_report(proposal_id=proposal_id)
    filename = print_and_save(report)
    return jsonify({"success": True, "filename": filename})


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")
