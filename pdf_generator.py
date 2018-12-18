import json
import csv
import uuid
import re
from pprint import pprint
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Frame, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from kafka import KafkaProducer
from wand.image import Image as WImage
styles = getSampleStyleSheet()

customStyle = ParagraphStyle(
   'Custom',
    parent = styles['Normal'],
    fontSize = 16,
    leading = 24
)

producer = KafkaProducer(bootstrap_servers='localhost:9092')

with open('data/ehr_samples.csv', 'r', encoding='utf8') as f:
    csv_reader = csv.reader(f)
    header = next(csv_reader)
    for row in csv_reader:
        specialty = re.sub('[^0-9a-zA-Z]+', '', row[3])
        pdf_filename = "data/pdf/" + specialty + "_" + row[0] + "_" + row[2] + ".pdf"

        doc = SimpleDocTemplate(pdf_filename)

        # print(pdf_filename)
        story = [Spacer(1, 1)]
        style = customStyle
        paragraph = Paragraph(row[5], style)
        story.append(paragraph)
        story.append(Spacer(1, 1))

        doc.build(story)

        jpg_file = pdf_filename[9:-4] + '.jpg'
        with WImage(filename=pdf_filename, resolution=300) as converted_image:
            converted_image.compression_quality = 99
            converted_image.save(filename='data/image/' + jpg_file)
            if len(converted_image.sequence) > 1:
                output_images = ['data/image/' + jpg_file[:-4] + '-{0.index}.jpg'.format(x) for x in converted_image.sequence]
            else:
                output_images = ['data/image/' + jpg_file]

        
        for output_image in output_images:
            message = {
                'image_name': output_image
            }
            producer.send("ehr-filestream", json.dumps(message).encode())
