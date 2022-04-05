import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

log = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TravelLog')


def get_latest_day(trip_name):
    try:
        response = table.query(
            Limit=1,
            ScanIndexForward=False,
            KeyConditionExpression=Key('TripName').eq(trip_name),
        )
    except ClientError as e:
        log.error(e.response['Error']['Message'])
    else:
        return int(response['Items'][0]['Day'])
