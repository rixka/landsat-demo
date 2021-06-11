import os
import boto3
import logging

from botocore import UNSIGNED
from botocore.config import Config
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

landsat_bucket = 'landsat-pds'
data_bucket = os.environ['IMAGE_BUCKET']

client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

def lambda_handler(event, context):
    landsat_keys = gen_keys(event['prefix'])

    return {
        'detail': {
            'landsat': landsat_keys
        }
    }


def gen_keys(prefix):

    now = datetime.today()
    today = now.strftime('%Y-%m-%d--%H%M')
    bucket = data_bucket + today + '/'

    return list_keys(prefix, now, bucket)


def list_keys(prefix, now, bucket):
    resp = client.list_objects_v2(Bucket=landsat_bucket, Prefix=prefix)

    logger.info("{} keys found".format(resp['KeyCount']))
    if resp['KeyCount'] > 0:
        keys = [
            {
                "key": 's3://{}/{}'.format(landsat_bucket, i['Key']),
                'bucket': bucket
            }
            for i in resp['Contents'] if i['Key'][-4:] == '.TIF'
            # if is_recent_object(datetime.today(), i['LastModified'])
        ]
    else:
        keys = []
    logger.info("Keys: {}".format(keys))
    return keys


def is_recent_object(now, set_date):
    checker = now-timedelta(hours=24)

    check_sec = checker.strftime('%s')
    now_sec = now.strftime('%s')
    sd_sec = set_date.strftime('%s')

    if check_sec <= sd_sec <= now_sec:
        # date less than 24 hours in the past
        return True
    else:
        return False

