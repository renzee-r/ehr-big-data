# MIDS 251 Project: EHR Big Data Pipeline

Image processing tool for Electronic Health Records (EHR) using Spark, HDFS, Tesseract, and ElasticSearch


# Introduction

## Setup Repo
1. Clone this repo
2. Import and activate the conda environment. All following steps must be done in this environment.

```bash
conda env create -f environment.yml
source activate ehr-big-data
```

## Setup MongoDB 
Need some content here

## How to Use 


### EAST
```bash
python text_detection.py --image examples/images/example_09.jpg --east frozen_east_text_detection.pb
```

### OCR
First, run the following to create a directory of PDF's.
```bash
python pdf_generator.py
```

Second, run the following to detect, decode, and upload predictions into a MongoDB.
```bash
python ocr_tesseract.py
```


