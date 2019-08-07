from util import RequestBody

from flask import render_template, make_response
import pdfkit


def create(reportCode, electionId, electorateId=None, officeId=None):
    html = render_template(
        'test-report-template.html',
        title="Test Template",
        data=[
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ]
    )

    options = {
        # Read more: https://wkhtmltopdf.org/usage/wkhtmltopdf.txt

        "page-size": "Legal",  # http://qt-project.org/doc/qt-4.8/qprinter.html#PaperSize-enum
        "orientation": "Landscape"  # Landscape or Portrait
    }

    pdf = pdfkit.from_string(html, False, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

    return response
