from os import environ
from io import BytesIO
from uuid import uuid4
from requests import post
from flask import Flask, jsonify, request
from mongoengine import connect

from reports.za import zonal_assignments_report
from reports.proposals import proposal_comments_report

app = Flask("office")

db_host = environ.get('DB_HOST', "localhost")
db_username = environ.get('MONGO_USERNAME')
db_password = environ.get('MONGO_PASSWORD')
db_auth_source = environ.get('MONGO_AUTH_SOURCE')
db_auth_mechanism = environ.get('MONGO_AUTH_MECHANISM')
connect("gem",
        host=db_host, username=db_username, password=db_password,
        authentication_source=db_auth_source,
        authentication_mechanism=db_auth_mechanism)


def print_and_save(content):
    stream = BytesIO(content.encode())
    files = {'file': stream}
    req = post("http://pdf-printer:4999/pdf", files=files)
    filename = str(uuid4()) + ".pdf"
    w = open("/usr/shared/downloads/" + filename, "wb")
    w.write(req.content)
    w.close()
    return filename


@app.route('/office/zonal/report', methods=['GET'])
def generate_zonal_report():
    hierarchy = request.args.get("hierarchy") in ["true", 1]
    leaves_only = request.args.get("leavesOnly") in ["true", 1]
    report = zonal_assignments_report(
        hierarchy=hierarchy, leaves_only=leaves_only)
    filename = print_and_save(report)
    return jsonify({"success": True, "filename": filename})


@app.route('/office/proposals/comments', methods=['GET'])
def generate_proposal_comments_report():
    proposal_id = request.args.get("proposal")

    report = proposal_comments_report(proposal_id=proposal_id)
    filename = print_and_save(report)
    return jsonify({"success": True, "filename": filename})

if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0")
