import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from wand.image import Image as WImage

pdf_file = 'Bariatrics_1_3.pdf'
jpg_file = pdf_file[:-4] + '.jpg'
with WImage(filename='pdf/' + pdf_file, resolution=300) as img:
    img.compression_quality = 99
    img.save(filename='image/' + jpg_file)
    if len(img.sequence) > 1:
        output_images = ['image/' + jpg_file[:-4] + '-{0.index}.jpg'.format(x) for x in img.sequence]
    else:
        output_images = ['image/' + jpg_file]

for oimg in output_images:  
    ocr_text = pytesseract.image_to_string(Image.open(oimg))

    txt_file = 'text/' + oimg[6:-4] + '.txt'
    with open(txt_file, 'w') as new_txt_file:
        new_txt_file.write(ocr_text.encode('utf-8'))
