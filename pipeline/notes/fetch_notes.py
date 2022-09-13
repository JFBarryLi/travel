import os
import re
import datetime
import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

log = logging.getLogger(__name__)

s3 = boto3.client('s3')
BUCKET = os.environ['NOTES_BUCKET_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TravelLog')


def get_note(key):
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=key)
    except ClientError as e:
        log.error(e.response['Error']['Message'])
    except Exception as e:
        log.error(f'Exception: {e}')
    else:
        return obj['Body'].read().decode('utf-8')


def list_notes(prefix_trip_name):
    if '/' not in prefix_trip_name:
        prefix_trip_name = prefix_trip_name + '/'

    try:
        objs = s3.list_objects_v2(
            Bucket=BUCKET, Prefix=prefix_trip_name, Delimiter='/'
        )
        notes = objs['Contents']
    except ClientError as e:
        log.error(e.response['Error']['Message'])
    except Exception as e:
        log.error(f'Exception: {e}')
    else:
        return notes


def get_latest_day(full_trip_name):
    try:
        response = table.query(
            Limit=1,
            ScanIndexForward=False,
            KeyConditionExpression=Key('TripName').eq(full_trip_name),
        )
    except ClientError as e:
        log.error(e.response['Error']['Message'])
    except Exception as e:
        log.error(f'Exception: {e}')
    else:
        if len(response['Items']) > 0:
            return int(response['Items'][0]['Day'])
        else:
            return 0


def parse_day(key):
    day = re.findall('[0-9]+', key.split('/')[-1])[0]
    return int(day)


def unprocessed_notes(objs, full_trip_name, process_all=False):
    # All notes with day greater than the day of the latest entry
    # on the dynamodb table, or with LastModified date greater than
    # the LastModified date on the latest entry are to be processed.

    latest_processed_day = get_latest_day(full_trip_name)

    try:
        if latest_processed_day > 0:
            latest_processed_obj = list(filter(
                lambda obj: parse_day(obj['Key']) == latest_processed_day, objs))[0]
            latest_processed_date = latest_processed_obj['LastModified']
        else:
            latest_processed_date = datetime.datetime(1, 1, 1)

        unprocessed = []
        for obj in objs:
            day = parse_day(obj['Key'])
            last_modified_date = obj['LastModified']
            if day > latest_processed_day or \
                    last_modified_date > latest_processed_date or \
                    process_all:
                unprocessed.append(obj['Key'])

        log.info(f'Unprocessed notes are: {unprocessed}')
    except Exception as e:
        log.error(f'Exception: {e}')
    return unprocessed
