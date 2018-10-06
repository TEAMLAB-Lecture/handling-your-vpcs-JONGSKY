import boto3


print("Write down the name of the bucket you want.")
BUCKET_NAME=input()


s3 = boto3.client('s3', region_name="ap-southeast-1")
response_list = s3.list_buckets()
buckets = [bucket['Name'] for bucket in response_list['Buckets']]


if BUCKET_NAME in buckets:
    print("already exist")
else:
    response = s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-southeast-1'
            }
        )
    print(BUCKET_NAME,"이 생성되었습니다.")
