import os
import boto3
import numpy
from uuid import uuid4
from PIL import Image

DB_TABLE = os.environ['DB_TABLE']

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DB_TABLE)

filepath = '/tmp/image.TIF'

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    s3.download_file(bucket, key, filepath)

    with Image.open(filepath) as im:
        imarray = numpy.array(im)

    put_metadata(imarray, bucket, key)

    return {
        'shape': imarray.shape,
        'size': imarray.size
    }


def put_metadata(imarray, bucket, key):
    uuid = str(uuid4())[0:8]

    response = table.put_item(
       Item={
            'id': uuid,
            'key': key,
            'bucket': bucket,
            'meta': {
                'shape': imarray.shape,
                'size': imarray.size
            }
        }
    )
