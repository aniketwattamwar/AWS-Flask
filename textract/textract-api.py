# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 12:09:52 2022

@author: hp
"""

ACCESS_KEY_ID='AKIAUUW4QZN3ONVOVTMQ'
ACCESS_SECRET_KEY='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'
#AWS_SESSION_TOKEN='FwoGZXIvYXdzEJz//////////wEaDMpLy934tam+4Epx5yLJATgiiL/fwKJfJ4wIiyvM8f6TXsfBjYnfqgBkWkYX4cL7s1l9UUtBPr2K64CjtGqhEq0mMd2ntXO7GvwwUK9xoVOTxEVHMuWJ4/pS5VGa3+kSn5EV+1XsS5gODHMa+qrJTcnCNTI4ySpS74T+780W7Ec/UCbFTtOEkTd6AcqSxS5PJQU9sGMO6dCOXZm7X1F/ZeFnd71p39kpbUrx5Qd3I747rix3U4IaunuKU/o0J0MTyacDCUoqEalnDT6uKcT0N5lEJzqhBjEJxiiB7KL4BTIt9zTZ4qq+Gq9j3vYQekfFvFfVYaohlgzlln1hhk0eLh+/IgXdC1EVaNPfP/Jb'

# import boto3

# # Document
# s3BucketName = "hs-textract"
# documentName = "simple-document-image.jpg"

# # Amazon Textract client
# textract = boto3.client('textract',
#                         aws_access_key_id=ACCESS_KEY_ID,
#                         aws_secret_access_key = ACCESS_SECRET_KEY, region_name='us-west-2')

# # Call Amazon Textract
# response = textract.detect_document_text(
#     Document={
#         'S3Object': {
#             'Bucket': s3BucketName,
#             'Name': documentName
#         }
#     })

# #print(response)

# # Print detected text
# for item in response["Blocks"]:
#     if item["BlockType"] == "LINE":
#         print (item["Text"])

import boto3
from trp import Document

# Document
documentName = "cheque.jpeg"

# Amazon Textract client
textract = boto3.client('textract',
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key = ACCESS_SECRET_KEY, region_name='us-west-2')

# Call Amazon Textract
with open(documentName, "rb") as document:
    response = textract.analyze_document(
        Document={
            
            'Bytes': document.read(),
        },
        FeatureTypes=["FORMS"])

#print(response)

doc = Document(response)

for page in doc.pages:
    
    key = "Pay"
    field = page.form.getFieldByKey(key)
    if(field):
        print("Key: {}, Value: {}".format(field.key, field.value))
    
    field_amt = page.form.searchFieldsByKey("Rupees")
    for f in field_amt:
        print("Key: {}, Value: {}".format(f.key, f.value))
    
    key = "A/c No"
    fields = page.form.searchFieldsByKey(key)
    for field in fields:
        print("Key: {}, Value: {}".format(field.key, field.value))