#!/usr/bin/env python3

import logging
from time import sleep

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import os


def replace_attribute(item, attribute_from, attribute_to):
    item[attribute_to] = item[attribute_from]
    del item[attribute_from]


def rename_attribute(dyn_table, attribute_from, attribute_to, pause_time):
    scan_filter = Attr(attribute_from).exists()

    response = dyn_table.scan(
        FilterExpression=scan_filter
    )

    sleep(pause_time)

    with dyn_table.batch_writer() as batch:
        logging.info(f"{len(response['Items'])} items to process.")
        for item in response['Items']:
            replace_attribute(item, attribute_from, attribute_to)
            batch.put_item(Item=item)

        while 'LastEvaluatedKey' in response:
            response = dyn_table.scan(
                FilterExpression=scan_filter,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )

            sleep(pause_time)

            for item in response['Items']:
                replace_attribute(item, attribute_from, attribute_to)
                batch.put_item(Item=item)


def table_rename_attribute(dyn_table, attribute_from, attribute_to):
    retry_exceptions = ('ProvisionedThroughputExceededException',
                        'ThrottlingException')
    retries = 0
    pause_time = 0

    while True:
        try:
            rename_attribute(dyn_table, attribute_from, attribute_to, pause_time)
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

    table_name = input('DynamoDB Table Name:')
    from_attribute = input('From Attribute:')
    to_attribute = input('To Attribute:')
    table_rename_attribute(DB.Table(table_name), from_attribute, to_attribute)

    logging.info('Processing Complete')
