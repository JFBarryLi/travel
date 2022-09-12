from decimal import Decimal
import boto3
import logging
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
DYNAMO_TABLE = os.environ['TRAVEL_TABLE']
travel_table = dynamodb.Table(DYNAMO_TABLE)


def put_log(processed_log):
    try:
        log.info(f"Uploading trip: {processed_log['trip_name']}, day: {processed_log['day']}, to dynamodb.")
        response = travel_table.put_item(
            Item={
                'TripName': processed_log['trip_name'],
                'Date': processed_log['date'],
                'Day': processed_log['day'],
                'StartLoc': processed_log['start_loc'],
                'StartLat': Decimal(str(processed_log['start_lat'])),
                'StartLng': Decimal(str(processed_log['start_lng'])),
                'EndLoc': processed_log['end_loc'],
                'EndLat': Decimal(str(processed_log['end_lat'])),
                'EndLng': Decimal(str(processed_log['end_lng'])),
                'WordCount': processed_log['word_count'],
                'CharacterCount': processed_log['character_count'],
                'SentenceCount': processed_log['sentence_count'],
                'Sentiment': processed_log['sentiment'],
            }
        )
    except ClientError as e:
        log.error(e.response['Error']['Message'])
    else:
        return response
