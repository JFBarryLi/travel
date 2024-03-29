import os
from datetime import datetime
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
        process_time = datetime.utcnow().isoformat()
        response = travel_table.put_item(
            Item={
                'TripName': processed_log['trip_name'],
                'Date': processed_log['date'],
                'Day': processed_log['day'],
                'StartLoc': processed_log['start_loc'],
                'StartLat': Decimal(str(processed_log['start_lat'])),
                'StartLng': Decimal(str(processed_log['start_lng'])),
                'StartCity': processed_log['start_city'],
                'StartState': processed_log['start_state'],
                'StartCountry': processed_log['start_country'],
                'StartCountryCode': processed_log['start_country_code'],
                'EndLoc': processed_log['end_loc'],
                'EndLat': Decimal(str(processed_log['end_lat'])),
                'EndLng': Decimal(str(processed_log['end_lng'])),
                'EndCity': processed_log['end_city'],
                'EndState': processed_log['end_state'],
                'EndCountry': processed_log['end_country'],
                'EndCountryCode': processed_log['end_country_code'],
                'WordCount': processed_log['word_count'],
                'CharacterCount': processed_log['character_count'],
                'SentenceCount': processed_log['sentence_count'],
                'Sentiment': processed_log['sentiment'],
                'ProccessTime': process_time,
            }
        )
    except ClientError as e:
        log.error(e.response['Error']['Message'])
    except Exception as e:
        log.error(f'Exception: {e}')
    else:
        return response
