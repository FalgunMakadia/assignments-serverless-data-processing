import json
import boto3
import mysql.connector

config = {
    'user': 'root',
    'password': 'rootroot',
    'host': 'named-entity-db.c2kjexpbd5qy.us-east-1.rds.amazonaws.com',
    'database': 'db-1'
}

mysql_connection = mysql.connector.connect(**config)

s3 = boto3.client('s3')


def entity_already_exists(entity_name):

    query = "SELECT * FROM named_entity_table WHERE entity_name = '{}'".format(entity_name)

    cursor = mysql_connection.cursor()
    cursor.execute(query)

    data = cursor.fetchall()
    return data


def db_ops(named_entities):

    for entity_name, freq in named_entities[next(iter(named_entities))].items():

        data = entity_already_exists(entity_name)
        cursor = mysql_connection.cursor()

        if len(data) != 0:
            query = "UPDATE named_entity_table SET freq = '{}' WHERE entity_name = '{}'".format(data[0][1] + freq,
                                                                                                  entity_name)
        else:
            query = "INSERT INTO named_entity_table VALUES ('{}', '{}')".format(entity_name, freq)

        cursor.execute(query)
        mysql_connection.commit()


def lambda_handler(event, context):
    bucketName = event['Records'][0]['s3']['bucket']['name']
    objectName = event['Records'][0]['s3']['object']['key']

    obj = s3.get_object(Bucket=bucketName, Key=objectName)
    fileData = obj['Body'].read().decode('utf-8')
    named_entities = json.loads(fileData)

    db_ops(named_entities)

    return {
        'statusCode': 200,
        'body': "Success"
    }
