import pytesseract
import pymongo
import bson
import json
import base64
import csv
import os
import requests
from PIL import Image, ImageEnhance, ImageFilter, ImageFile
from wand.image import Image as WImage
from bson.codec_options import CodecOptions
from io import BytesIO
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import udf, from_json, lit
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
ImageFile.LOAD_TRUNCATED_IMAGES = True

# client = pymongo.MongoClient("mongodb+srv://admin-1:JK6qJJz4lVUmDp2J@w251-ehr-project-weita.mongodb.net/ehr?retryWrites=true")
# db = client.ehr
# collection = db.ocrdata

def file_schema():
    """
    root
    |-- image_name: string (nullable = false)
    """
    return StructType([
        StructField("image_name", StringType(), False),
    ])

def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("EhrFileProcessingJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "ehr-filestream") \
        .load()
    

    # Create a stream for buy events
    file_events = raw_events \
        .select(from_json(raw_events.value.cast('string'), file_schema()).alias('json'),
                raw_events.timestamp.cast('string')) \
        .select('json.image_name', 'timestamp')

    udfOcrExtraction = udf(ocrExtraction, StringType())
    file_events_ocr = file_events \
        .withColumn("image_text", udfOcrExtraction(file_events.image_name))

    udfEncodeFile = udf(encodeFile, StringType())
    file_events_encode = file_events_ocr \
        .withColumn("image_file", udfEncodeFile(file_events.image_name))

    sink = file_events_encode \
        .writeStream \
        .format("json") \
        .option("checkpointLocation", "/tmp/checkpoints_file_events") \
        .option("path", "/tmp/json") \
        .trigger(processingTime="10 seconds") \
        .start()

    sink.awaitTermination()


def ocrExtraction(image_name):
    with Image.open('/home/kafka/ehr/' + image_name) as image_reader:
        return pytesseract.image_to_string(image_reader)


def encodeFile(image_name):
    with Image.open('/home/kafka/ehr/' + image_name) as image_reader:
        image_buffer = BytesIO()
        image_reader.save(image_buffer, format="JPEG")
        image_str = base64.b64encode(image_buffer.getvalue())
        return str(image_str).encode('utf-8')


if __name__ == "__main__":
    main()

