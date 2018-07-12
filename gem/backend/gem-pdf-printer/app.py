from logging import debug
from weasyprint import HTML
from flask import Flask, request, make_response
from logging.config import fileConfig

fileConfig('logging.conf')
app = Flask('pdf')


@app.route('/pdf', methods=['POST'])
def generate():
    name = request.args.get('filename', 'unnamed.pdf')
    debug("Printing pdf '%s'", name)

    file_data = request.files["file"].read()
    html = HTML(string=file_data)
    pdf = html.write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=%s' % name
    return response


if __name__ == '__main__':
    app.run()
