
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_report(data):

    file = "reports/security_report.pdf"

    styles = getSampleStyleSheet()

    elements = []

    for item in data:

        text = f"{item['file']} - {item['issue']}"

        elements.append(Paragraph(text, styles["Normal"]))

    pdf = SimpleDocTemplate(file)

    pdf.build(elements)

    return file
