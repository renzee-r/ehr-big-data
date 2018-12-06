import pytesseract
import pymongo
import bson
import base64
import csv
from PIL import Image, ImageEnhance, ImageFilter
from wand.image import Image as WImage
from bson.codec_options import CodecOptions
from io import BytesIO

client = pymongo.MongoClient("mongodb+srv://admin-1:JK6qJJz4lVUmDp2J@w251-ehr-project-weita.mongodb.net/ehr?retryWrites=true")
db = client.ehr
collection = db.ocrdata

pdf_file = 'Bariatrics_1_3.pdf'
jpg_file = pdf_file[:-4] + '.jpg'
with WImage(filename='pdf/' + pdf_file, resolution=300) as converted_image:
    converted_image.compression_quality = 99
    converted_image.save(filename='image/' + jpg_file)
    if len(converted_image.sequence) > 1:
        output_images = ['image/' + jpg_file[:-4] + '-{0.index}.jpg'.format(x) for x in converted_image.sequence]
    else:
        output_images = ['image/' + jpg_file]

for output_image in output_images: 
    with Image.open(output_image) as image_reader:
        ocr_text = pytesseract.image_to_string(image_reader)

        # txt_file = 'text/' + output_image[6:-4] + '.txt'
        # with open(txt_file, 'w') as new_txt_file:
        #     new_txt_file.write(ocr_text.encode('utf-8'))

        ocr_data = pytesseract.image_to_data(image_reader, nice=1).encode('utf-8', 'strict')

        # txt_file = 'text-data/' + output_image[6:-4] + '.txt'
        # with open(txt_file, 'w') as new_txt_file:
        #     new_txt_file.write(ocr_data.encode('utf-8'))

        # Cnvert ocr data into json
        ocr_json = {}
        ocr_reader = csv.reader(ocr_data.splitlines(), delimiter='\t')
        header_flag = 1
        for row in ocr_reader:
            # Skip the header row
            if header_flag == 1:
                header_flag = 0
                continue
            
            # Skip rows without text
            if row[10] == "-1":
                continue

            ocr_key = row[11].replace('.', '').replace('$', '')

            ocr_value = {
                    "page_num": row[1]
                    ,"block_num": row[2]
                    ,"par_num": row[3]
                    ,"line_num": row[4]
                    ,"word_num": row[5]
                    ,"left": row[6]
                    ,"top": row[7]
                    ,"width": row[8]
                    ,"height": row[9]
                }

            if ocr_key in ocr_json:
                ocr_json[ocr_key].append(ocr_value)
            else:
                ocr_json[ocr_key] = [ocr_value]
            

        image_buffer = BytesIO()
        image_reader.save(image_buffer, format="JPEG")
        image_str = base64.b64encode(image_buffer.getvalue())
    
        mongo_row = {
            'image_name': output_image
            ,'image_file': image_str
            ,'ocr_text': ocr_text.encode('utf-8', 'strict')
            ,'ocr_data': ocr_json
        }

        # print(mongo_row)
        mongo_row_id = collection.insert_one(mongo_row).inserted_id

        # print(row_id)

    
