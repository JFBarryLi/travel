#!/usr/bin/env python3

import logging
from time import sleep

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import os


def copy_to_new_table(table_old, table_new, pause_time):

    table_old_response = table_old.scan()

    sleep(pause_time)

    with table_new.batch_writer() as batch:
        logging.info(f"{len(table_old_response['Items'])} items to process.")
        for item in table_old_response['Items']:
            item['PK'] = 'UserId:028d17d8-8ec1-4a60-8995-f2f4dfb1ac80'
            SK = f"TripName:{item['TripName']}#Date:{item['Date']}"
            item['SK'] = SK

            logging.info(f'Processing: {SK}')
            batch.put_item(Item=item)

        while 'LastEvaluatedKey' in table_old_response:
            table_old_response = table_old.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
            )

            sleep(pause_time)

            for item in table_old_response['Items']:
                item['PK'] = 'UserId:028d17d8-8ec1-4a60-8995-f2f4dfb1ac80'
                SK = f"TripName:{item['TripName']}#Date:{item['Date']}"
                item['SK'] = SK

                logging.info(f'Processing: {SK}')
                batch.put_item(Item=item)


def table_copy(table_old, table_new):
    retry_exceptions = ('ProvisionedThroughputExceededException',
                        'ThrottlingException')
    retries = 0
    pause_time = 0

    while True:
        try:
            copy_to_new_table(table_old, table_new, pause_time)
            break
        except ClientError as err:
            if err.response['Error']['Code'] not in retry_exceptions:
                raise
            pause_time = (2 ** retries)
            logging.info('Back-off set to %d seconds', pause_time)
            retries += 1


if __name__ == '__main__':
    logging.getLogger('').setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    DB = boto3.resource('dynamodb')

    table_old = input('Old Table:')
    table_new = input('New Table:')
    table_copy(DB.Table(table_old), DB.Table(table_new))

    logging.info('Processing Complete')
