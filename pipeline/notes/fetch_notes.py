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


def get_table(full_trip_name):
    try:
        response = table.query(
            ScanIndexForward=False,
            KeyConditionExpression=Key('TripName').eq(full_trip_name),
        )
        if len(response['Items']) > 0:
            items = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.query(
                ScanIndexForward=False,
                KeyConditionExpression=Key('TripName').eq(full_trip_name),
            )
            if len(response['Items']) > 0:
                items += response['Items']

    except ClientError as e:
        log.error(e.response['Error']['Message'])
    except Exception as e:
        log.error(f'Exception: {e}')
    else:
        return items


def get_latest_day(table):
    if len(table) > 0:
        return int(max([r['Day'] for r in table]))
    else:
        return 0


def parse_day(key):
    day = re.findall('[0-9]+', key.split('/')[-1])[0]
    return int(day)


def unprocessed_notes(objs, full_trip_name, process_all=False):
    # All notes with day greater than the day of the latest entry
    # on the dynamodb table, or with LastModified date greater than
    # the LastModified date on the latest entry are to be processed.
    # All notes that are on s3 but not on the DyanmoDB table are to
    # be processed.

    table = get_table(full_trip_name)
    latest_processed_day = get_latest_day(table)

    try:
        if latest_processed_day > 0:
            latest_processed_obj = list(filter(
                lambda obj: parse_day(obj['Key']) == latest_processed_day, objs))[0]
            latest_processed_date = latest_processed_obj['LastModified']
        else:
            latest_processed_date = datetime.datetime(1, 1, 1)

        table_days = [int(item['Day']) for item in table]

        unprocessed = []
        for obj in objs:
            day = parse_day(obj['Key'])
            last_modified_date = obj['LastModified']
            if day > latest_processed_day or \
                    last_modified_date > latest_processed_date or \
                    day not in table_days or \
                    process_all:
                unprocessed.append(obj['Key'])

        log.info(f'Unprocessed notes are: {unprocessed}')
    except Exception as e:
        log.error(f'Exception: {e}')
    return unprocessed
