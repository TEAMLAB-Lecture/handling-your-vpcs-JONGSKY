import boto3
from botocore.exceptions import ClientError
import time
import logging
import random
import botocore
import os

def vpc_creation():
    ec2 = boto3.client('ec2')

    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('sg-7dc58c05', '')

    hdlr = logging.FileHandler('vpc.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s')
    hdlr.setFormatter(formatter)

    TCP = [1,7,9,13,17,19,20,21,22,23,24,25,37,53,70,79,80,88]
    UDP = [7,9,13,19,37,49,53,67,68,69,80]


    try:
        for i in range(0,10):
            response = ec2.create_security_group(GroupName=str(i)+'HelloBOTO',
                                                 Description='Made by boto3',
                                                 VpcId=vpc_id)
            security_group_id = response['GroupId']
            print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
            TCP_Port = TCP[random.randrange(18)]
            UDP_Port = UDP[random.randrange(11)]
            data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': TCP_Port,
                     'ToPort': TCP_Port,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'udp',
                     'FromPort': UDP_Port,
                     'ToPort': UDP_Port,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
            print('Ingress Successfully Set %s' % data)


            logger = logging.getLogger(security_group_id)
            logger.addHandler(hdlr)
            logger.setLevel(logging.INFO)
            logger.info('create'.format())

            timeout = time.time() + 5
            while True:
                if time.time() >= timeout:
                    break
    except ClientError as e:
        logger.error('create_error'.format(e,))

def vpc_delete():
    client = boto3.client('ec2')
    ec2 = boto3.client('ec2')
    result = client.describe_security_groups()
    hdlr = logging.FileHandler('vpc.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s')
    hdlr.setFormatter(formatter)

    try:
        for i in result["SecurityGroups"]:
            if i["GroupName"]=="launch-wizard-1":
                pass
            elif i["GroupName"]=="launch-wizard-2":
                pass
            elif i["GroupName"]=="default":
                pass
            else:
                ec2.delete_security_group(GroupName=i["GroupName"])
                print('Security Group Deleted')
                logger = logging.getLogger(i["GroupId"])
                logger.addHandler(hdlr)
                logger.setLevel(logging.INFO)
                logger.info('delete'.format())

    except ClientError as e:
        logger.error('delete_error'.format(e,))

def create_s3_bucket():

    BUCKET_NAME = 'jongsky-bucket'


    s3 = boto3.client('s3', region_name="ap-southeast-1")
    response_list = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response_list['Buckets']]


    if BUCKET_NAME in buckets:
        pass
    else:
        response = s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-southeast-1'
                }
            )
        print(BUCKET_NAME,"이 생성되었습니다.")

def upload_s3_logfile():
    KEY = 'vpc.log'
    s3 = boto3.resource('s3')
    s3_1 = boto3.client('s3')
    response_list = s3_1.list_buckets()
    buckets = [bucket['Name'] for bucket in response_list['Buckets']]



    BUCKET_NAME = 'jongsky-bucket'

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


if __name__ == '__main__':
    vpc_creation()
    vpc_delete()
    create_s3_bucket()
    upload_s3_logfile()
