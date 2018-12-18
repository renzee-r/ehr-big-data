import pytesseract
import pymongo
import bson
import json
import base64
import csv
import os
import requests
from PIL import Image, ImageEnhance, ImageFilter
from wand.image import Image as WImage
from bson.codec_options import CodecOptions
from io import BytesIO

# client = pymongo.MongoClient("mongodb+srv://admin-1:JK6qJJz4lVUmDp2J@w251-ehr-project-weita.mongodb.net/ehr?retryWrites=true")
# db = client.ehr
# collection = db.ocrdata

json_data = []
file_counter = 0
for pdf_file in os.listdir('data/pdf'):
    if not pdf_file.endswith('.pdf'):
        continue

    print('Processing file: ' + pdf_file)
    file_counter += 1

    jpg_file = pdf_file[:-4] + '.jpg'
    with WImage(filename='data/pdf/' + pdf_file, resolution=300) as converted_image:
        converted_image.compression_quality = 99
        converted_image.save(filename='data/image/' + jpg_file)
        if len(converted_image.sequence) > 1:
            output_images = ['data/image/' + jpg_file[:-4] + '-{0.index}.jpg'.format(x) for x in converted_image.sequence]
        else:
            output_images = ['data/image/' + jpg_file]

    for output_image in output_images:
        with Image.open(output_image) as image_reader:
            ocr_text = pytesseract.image_to_string(image_reader)

            # ocr_data = pytesseract.image_to_data(image_reader)
            # # Convert ocr data into json
            # ocr_json = {}
            # ocr_reader = csv.reader(ocr_data.splitlines(), delimiter='\t')
            # header_flag = 1
            # for row in ocr_reader:
            #     # Skip the header row
            #     if header_flag == 1:
            #         header_flag = 0
            #         continue

            #     # Skip rows without text
            #     if row[10] == "-1":
            #         continue

            #     ocr_key = row[11].replace('.', '').replace('$', '')

            #     ocr_value = {
            #         "page_num": row[1]
            #         ,"block_num": row[2]
            #         ,"par_num": row[3]
            #         ,"line_num": row[4]
            #         ,"word_num": row[5]
            #         ,"left": row[6]
            #         ,"top": row[7]
            #         ,"width": row[8]
            #         ,"height": row[9]
            #     }

            #     if ocr_key in ocr_json:
            #         ocr_json[ocr_key].append(ocr_value)
            #     else:
            #         ocr_json[ocr_key] = [ocr_value]


            image_buffer = BytesIO()
            image_reader.save(image_buffer, format="JPEG")
            image_str = base64.b64encode(image_buffer.getvalue())

            json_row = {
                'image_name': output_image
                ,'image_file': str(image_str, 'utf-8')
                ,'ocr_text': ocr_text
                # ,'ocr_data': ocr_json
            }

            json_data.append(json_row)

            # if file_counter % 5 == 0:
            #     with open('data/json/ehr_samples_' + str(file_counter / 5)  + '.json', 'w') as json_file:
            #         json.dump(json_data, json_file) 

            url = 'http://169.53.145.101:9200/ehr/image'
            payload = json.dumps(json_row)
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            r = requests.post(url, data=payload, headers=headers)
            print(r.text)

            # mongo_row_id = collection.insert_one(mongo_row).inserted_id
            # print(row_id)


            

