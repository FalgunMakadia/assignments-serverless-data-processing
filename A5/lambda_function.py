import json
import boto3
import os

def lambda_handler(event, context):
	for record in event['Records']:
		send_request(record['body'])

def send_request(body):
	sns_client = boto3.client('sns')

	res = sns_client.publish(TopicArn = 'arn:aws:sns:us-east-1:916314196979:HalifaxFlowersSNS', Message = body)
	print(res)
