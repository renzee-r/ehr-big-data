import json
import csv
import uuid
import re
from pprint import pprint
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Frame, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
styles = getSampleStyleSheet()

customStyle = ParagraphStyle(
   'Custom',
    parent = styles['Normal'],
    fontSize = 16,
    leading = 24
)

with open('data/ehr_samples.csv', 'r', encoding='utf8') as f:
    csv_reader = csv.reader(f)
    header = next(csv_reader)
    for row in csv_reader:
        specialty = re.sub('[^0-9a-zA-Z]+', '', row[3])
        filename = "pdf/" + specialty + "_" + row[0] + "_" + row[2] + ".pdf"

        doc = SimpleDocTemplate(filename)

        # print(filename)
        story = [Spacer(1, 1)]
        style = customStyle
        paragraph = Paragraph(row[5], style)
        story.append(paragraph)
        story.append(Spacer(1, 1))

        doc.build(story)