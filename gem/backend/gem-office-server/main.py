from os import environ
from io import BytesIO
from requests import post
from flask import Flask, jsonify
from mongoengine import connect

from reports.za import zonal_assignments_report

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
    req = post("http://gem-pdf-printer:4999/pdf", files=files)
    w = open('/data/files/001.pdf', 'wb')
    w.write(req.content)
    w.close()


@app.route('/office/zonal/report', methods=['GET'])
def generate_zonal_report():
    report = zonal_assignments_report()
    print_and_save(report)
    return jsonify({"success": True, "path": "001.pdf"})


if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0")
