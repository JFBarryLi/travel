import boto3
import logging
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TravelLog')


def put_log(processed_log):
    try:
        response = table.put_item(
            Item={
                'TripName': processed_log['trip_name'],
                'Date': processed_log['date'],
                'Day': processed_log['day'],
                'StartLoc': processed_log['start_loc'],
                'StartLat': processed_log['start_lat'],
                'StartLng': processed_log['start_lng'],
                'EndLoc': processed_log['end_loc'],
                'EndLat': processed_log['end_lat'],
                'EndLng': processed_log['end_lng'],
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
