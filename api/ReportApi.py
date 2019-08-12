from util import RequestBody

from flask import render_template, make_response
import pdfkit


def create(reportCode, electionId, electorateId=None, officeId=None):
    html = render_template(
        'pre-41.html',
        content={
            "title": "PRESIDENTIAL ELECTION ACT NO. 15 OF 1981",
            "electoralDistrict": "1. Matara",
            "pollingDivision": "Division 1",
            "pollingDistrictNos": "1, 2, 3, 4",
            "countingHallNo": "1",
            "data": [
                       [1, "Yujith Waraniyagoda", "Moon", "Five Hundred", 500, "Saman"],
                       [2, "Clement Fernando", "Bottle", "Five Hundred", 500, "Saman"],
                       [3, "Umayanga Gunewardena", "Python", "Five Hundred", 500, "Saman"],
                       [4, "Sherazad Hamit", "Hammer", "Five Hundred", 500, "Saman"],
                       [5, "Anushka", "Carrot", "Five Hundred", 500, "Saman"],
                       [6, "Samudra Weerasinghe", "Fish", "Five Hundred", 500, "Saman"]
                   ],
            "total": 3000,
            "rejectedVotes": 50,
            "grandTotal": 3050
        }
    )


    options = {
        # Read more: https://wkhtmltopdf.org/usage/wkhtmltopdf.txt

        "page-size": "A3",  # http://qt-project.org/doc/qt-4.8/qprinter.html#PaperSize-enum
        "orientation": "Portrait"  # Landscape or Portrait
    }

    pdf = pdfkit.from_string(html, False, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

    return response
