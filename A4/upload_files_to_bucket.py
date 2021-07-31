import boto3
from botocore.exceptions import ClientError
import os
import time

BUCKET_NAME = 'sourcedatab00874635'

s3 = boto3.client('s3')

def upload_file_to_bucket(file, bucketName, fileName):
	try:
		s3.upload_file(file, bucketName, fileName)
		print(fileName + ' File uploaded Successfully!')
	except ClientError as ce:
		print(fileName + ' File upload Failed!: ' + ce)


def initiate_file_upload():
	path = 'Dataset/Train/'
	dirr = os.fsencode(path)

	for file in os.listdir(dirr):
		fileName = os.fsdecode(file)
		upload_file_to_bucket(path + fileName, BUCKET_NAME, fileName)

initiate_file_upload()
