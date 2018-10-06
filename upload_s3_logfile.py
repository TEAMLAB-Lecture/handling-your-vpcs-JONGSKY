import boto3
import botocore
import os

KEY = 'vpc.log'
s3 = boto3.resource('s3')
s3_1 = boto3.client('s3')
response_list = s3_1.list_buckets()
buckets = [bucket['Name'] for bucket in response_list['Buckets']]


print("Write yout Bucket name")
BUCKET_NAME=input()

if BUCKET_NAME in buckets:
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, 'down.log')
        f = open("vpc.log", 'r')
        data = f.read()
        ff = open("down.log", 'r')
        down_data = ff.read()
        if data == down_data:
            f.close()
            ff.close()
            os.remove('down.log')
            print("이미 log파일이 최신버전입니다.")
        else:
            f_read=open("vpc.log", 'r').readlines()
            out=open("down.log", 'w')
            for line in f_read:
                out.write(line)
            files = os.listdir("./")
            f.close()
            ff.close()
            out.close()
            for filename in files:
                if filename == "down.log":
                    down_data=open("down.log", 'r')
                    s3_1.upload_file(filename, BUCKET_NAME, KEY)
                    down_data.close()
                    os.remove('down.log')
                    print("log파일을 최신버전으로 업로드했습니다.")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            files = os.listdir("./")
            for filename in files:
                if filename == 'vpc.log':
                    s3_1.upload_file(filename, BUCKET_NAME, KEY)
                    print("새로운 log파일을 업로드했습니다.")
        else:
            raise
else:
    print(BUCKET_NAME,"으로 된 버킷이 없습니다.")
