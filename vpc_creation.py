import boto3
from botocore.exceptions import ClientError
import time
import logging
import random

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
        TCP_Port = TCP[random.randrange(19)]
        UDP_Port = UDP[random.randrange(12)]
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
