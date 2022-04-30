
from flask import Flask, render_template, request,jsonify
import boto3
app = Flask(__name__)
from werkzeug.utils import secure_filename
from trp import Document
from collections import OrderedDict

ACCESS_KEY_ID=<add-key>
ACCESS_SECRET_KEY=<add-secret-key>

s3 = boto3.client('s3',
                    aws_access_key_id=ACCESS_KEY_ID,
                    aws_secret_access_key= ACCESS_SECRET_KEY,
                                   )

textract = boto3.client('textract',
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key = ACCESS_SECRET_KEY, region_name='us-west-2')

BUCKET_NAME = "hs-textract"
 
@app.route('/')  
def home():
    return render_template("file_upload_to_s3.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file( 
                Bucket = BUCKET_NAME,
                Filename=filename,
                Key = filename
            )
            msg = "Upload Done ! "

    return render_template("file_upload_to_s3.html",msg =msg)


@app.route('/extract', methods=['post'])
def extract():
    if request.method == 'POST':
      
        objs = s3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter='/') ['Contents']
        print(objs)
        objs.sort(key=lambda e: e['LastModified'], reverse=True)
        print("******")
        print(objs[0])
        first_item = list(objs[0].items())[0]
        print(first_item[1])
        documentName = str(first_item[1])
        
        # Call Amazon Textract
        with open(documentName, "rb") as document:
            response = textract.analyze_document(
                Document={
                    
                    'Bytes': document.read(),
                },
                FeatureTypes=["FORMS"])
        
        doc = Document(response)
        text = []
        for page in doc.pages:
            
            key = "Pay"
            field = page.form.getFieldByKey(key)
            if(field):
                print("Key: {}, Value: {}".format(field.key, field.value))
            
            field_amt = page.form.searchFieldsByKey("Rupees")
            for f in field_amt:
                print("Key: {}, Value: {}".format(f.key, f.value))
                text.append(f.key)
                text.append(f.value)

            print(text)
            key = "A/c No"
            fields = page.form.searchFieldsByKey(key)

            for field in fields:
                print("Key: {}, Value: {}".format(field.key, field.value))
                text.append(field.key)
                text.append(field.value)

    return render_template("file_upload_to_s3.html",text = text)


if __name__ == "__main__":
    
    app.run(debug=True)


