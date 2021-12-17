
from flask import Flask, render_template, request
import boto3
app = Flask(__name__)
from werkzeug.utils import secure_filename
# import key_config as keys

s3 = boto3.client('s3',
                    aws_access_key_id='put-id-here',
                    aws_secret_access_key='put-key-here'
                      )
# s3 = boto3.client('s3')
BUCKET_NAME='lambda-s3-hs'

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




if __name__ == "__main__":
    
    app.run(debug=True)





# import json
# import boto3

# s3 = boto3.resource('s3')
# sns = boto3.client('sns')

# def lambda_handler(event,context):
     
#     bkt = s3.Bucket('lambda-s3-hs')
#     count =0
#     for obj in bkt.objects.all():
#         count+=1
#         print(obj.key)
#     print(count)
#     if count != 0:
#         print('Object found. Sending notification')
#         sns.publish(TopicArn='arn:aws:sns:us-east-1:405259030962:notif',Message='The file is uploaded. The number of submissions received are ' + str(count) , Subject='Submission received')
#     else:
#         print('File was not present')
        