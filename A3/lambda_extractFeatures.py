import json
import boto3

s3 = boto3.client('s3')

BUCKET_NAME = 'tagsb00874635'


def lambda_handler(event, context):
    bucketName = event['Records'][0]['s3']['bucket']['name']
    objectName = event['Records'][0]['s3']['object']['key']

    obj = s3.get_object(Bucket=bucketName, Key=objectName)
    dataFromFile = obj['Body'].read().decode('utf-8')
    dataFromFile = dataFromFile.replace('\n', ' ')

    namedEntities = {}

    for word in dataFromFile.split(' '):

        word = word.strip()

        if word[0].isupper():
            if word in namedEntities:
                namedEntities[word] += 1
            else:
                namedEntities[word] = 1

    fileNameForSecondBucket = objectName.split('.')[0] + 'ne'
    newFileData = {fileNameForSecondBucket: namedEntities}
    fileNameForSecondBucket += '.txt'

    s3.put_object(
        Bucket = BUCKET_NAME,
        Body = json.dumps(newFileData),
        Key = fileNameForSecondBucket
    )

    return {
        'statusCode': 200,
        'body': json.dumps(fileNameForSecondBucket + ' File uploaded Successfully!')
    }
