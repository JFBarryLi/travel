#!/usr/bin/env python3
import boto3
import logging
from decimal import Decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

from pipeline.notes.geo_code import geo_code

log = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TravelLog')

overrides = [
    {
        'filter_expr': 'StartCity = :StartCity and StartCountry = :StartCountry',
        'expr_attr_vals': {
            ':StartCity': 'Lagos',
            ':StartCountry': 'Nigeria',
        },
        'override_value': 'Lagos Portugal',
        'field': 'start_location',
    },
    {
        'filter_expr': 'EndCity = :EndCity and EndCountry = :EndCountry',
        'expr_attr_vals': {
            ':EndCity': 'Lagos',
            ':EndCountry': 'Nigeria',
        },
        'override_value': 'Lagos Portugal',
        'field': 'end_location',
    },
]


def get_keys(full_trip_name, filter_expr, expr_attr_vals):
    try:
        log.info('Getting keys.')
        keys = []
        response = table.query(
            KeyConditionExpression=Key('TripName').eq(full_trip_name),
            FilterExpression=filter_expr,
            ExpressionAttributeValues=expr_attr_vals,
        )
        if len(response['Items']) > 0:
            keys = [{'TripName': item['TripName'], 'Date': item['Date']} for item in response['Items']]

        while 'LastEvaluatedKey' in response:
            response = table.query(
                KeyConditionExpression=Key('TripName').eq(full_trip_name),
                FilterExpression=filter_expr,
                ExpressionAttributeValues=expr_attr_vals,
                ExclusiveStartKey=response['LastEvaluatedKey'],
            )
            if len(response['Items']) > 0:
                keys += [{'TripName': item['TripName'], 'Date': item['Date']} for item in response['Items']]
    except ClientError as e:
        log.error(e.response['Error']['Message'])
    except Exception as e:
        log.error(f'Exception: {e}')
    else:
        return keys


def get_new_location(override_value):
    log.info('Geo-coding with new override values.')
    location = geo_code(override_value)
    return location


def update_table(full_trip_name):
    for override in overrides:
        keys = get_keys(
            full_trip_name,
            override['filter_expr'],
            override['expr_attr_vals']
        )

        override_loc = get_new_location(override['override_value'])

        if override['field'] == 'start_location':
            prefix = 'Start'
        else:
            prefix = 'End'

        update_expr = f'SET {prefix}Lat = :lat, ' + \
            f'{prefix}Lng = :lng, ' + \
            f'{prefix}City = :city, ' + \
            f'{prefix}State = :state, ' + \
            f'{prefix}Country = :country, ' + \
            f'{prefix}CountryCode = :country_code'

        log.info(f'Update Expression: {update_expr}.')

        expr_attr_vals = {
            ':lat': Decimal(str(override_loc['latitude'])),
            ':lng': Decimal(str(override_loc['longitude'])),
            ':city': override_loc['city'],
            ':state': override_loc['state'],
            ':country': override_loc['country'],
            ':country_code': override_loc['country_code']
        }
        log.info(f'Expression Attribute Values: {expr_attr_vals}')

        for key in keys:
            try:
                log.info(f"Updating {key['TripName']} - {key['Date']}")
                update = table.update_item(
                    Key={
                        'TripName': key['TripName'],
                        'Date': key['Date'],
                    },
                    UpdateExpression=update_expr,
                    ExpressionAttributeValues=expr_attr_vals,
                )
            except ClientError as e:
                log.error(e.response['Error']['Message'])
            except Exception as e:
                log.error(f'Exception: {e}')


update_table('World Tour 2021-2023')
