from io import BytesIO
from requests import post
from flask import Flask, jsonify

from reports.za import zonal_assignments_report

app = Flask("office")


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
    app.run()
