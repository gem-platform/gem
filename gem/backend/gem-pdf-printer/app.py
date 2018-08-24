"""PDF printing service."""

from logging import debug
from logging.config import fileConfig

from weasyprint import HTML
from flask import Flask, request, make_response

fileConfig('logging.conf')
app = Flask('pdf')


@app.route('/pdf', methods=['POST'])
def generate():
    """Generate PDF using specified data."""
    # get request data
    name = request.args.get('filename', 'unnamed.pdf')
    file_data = request.files["file"].read()

    # generate pdf file
    debug("Printing pdf '%s'", name)
    html = HTML(string=file_data)
    pdf = html.write_pdf()

    # send response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=%s' % name
    return response


if __name__ == '__main__':
    app.run()
