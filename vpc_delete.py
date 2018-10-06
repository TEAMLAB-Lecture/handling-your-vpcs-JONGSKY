import boto3
from botocore.exceptions import ClientError
import logging

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
