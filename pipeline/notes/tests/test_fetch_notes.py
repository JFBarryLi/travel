import datetime
from dateutil.tz import tzutc
from unittest.mock import patch

from ..fetch_notes import parse_day, unprocessed_notes


def test_parse_day():
    key = 'world-tour/day512.txt'
    assert parse_day(key) == 512


@patch('pipeline.notes.fetch_notes.get_table')
@patch('pipeline.notes.fetch_notes.get_latest_day')
def test_unprocessed_notes_regular(mock_get_latest_day, mock_get_table):
    mock_get_latest_day.return_value = 3
    mock_get_table.return_value = [
        {'Day': 1}, {'Day': 2}, {'Day': 3}, {'Day': 4}, {'Day': 5}
    ]

    notes = [
        {
            'Key': 'world-tour/day1.txt',
            'LastModified': datetime.datetime(2022, 4, 7, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day2.txt',
            'LastModified': datetime.datetime(2022, 4, 8, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day3.txt',
            'LastModified': datetime.datetime(2022, 4, 9, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day4.txt',
            'LastModified': datetime.datetime(2022, 4, 10, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day5.txt',
            'LastModified': datetime.datetime(2022, 4, 11, 0, 0, 0, tzinfo=tzutc())
        }
    ]

    up_notes = unprocessed_notes(notes, 'trip_name')
    assert up_notes == ['world-tour/day4.txt', 'world-tour/day5.txt']


@patch('pipeline.notes.fetch_notes.get_table')
@patch('pipeline.notes.fetch_notes.get_latest_day')
def test_unprocessed_notes_last_modified_date(mock_get_latest_day, mock_get_table):
    mock_get_latest_day.return_value = 4
    mock_get_table.return_value = [
        {'Day': 1}, {'Day': 2}, {'Day': 3}, {'Day': 4}, {'Day': 5}
    ]

    notes = [
        {
            'Key': 'world-tour/day1.txt',
            'LastModified': datetime.datetime(2022, 4, 7, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day2.txt',
            'LastModified': datetime.datetime(2022, 4, 8, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day3.txt',
            'LastModified': datetime.datetime(2022, 4, 11, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day4.txt',
            'LastModified': datetime.datetime(2022, 4, 10, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day5.txt',
            'LastModified': datetime.datetime(2022, 4, 11, 0, 0, 0, tzinfo=tzutc())
        }
    ]

    up_notes = unprocessed_notes(notes, 'trip_name')
    assert up_notes == ['world-tour/day3.txt', 'world-tour/day5.txt']


@patch('pipeline.notes.fetch_notes.get_table')
@patch('pipeline.notes.fetch_notes.get_latest_day')
def test_unprocessed_notes_process_all(mock_get_latest_day, mock_get_table):
    mock_get_latest_day.return_value = 4
    mock_get_table.return_value = [
        {'Day': 1}, {'Day': 2}, {'Day': 3}, {'Day': 4}, {'Day': 5}
    ]

    notes = [
        {
            'Key': 'world-tour/day1.txt',
            'LastModified': datetime.datetime(2022, 4, 7, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day2.txt',
            'LastModified': datetime.datetime(2022, 4, 8, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day3.txt',
            'LastModified': datetime.datetime(2022, 4, 11, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day4.txt',
            'LastModified': datetime.datetime(2022, 4, 10, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day5.txt',
            'LastModified': datetime.datetime(2022, 4, 11, 0, 0, 0, tzinfo=tzutc())
        }
    ]

    up_notes = unprocessed_notes(notes, 'trip_name', process_all=True)
    assert up_notes == [
            'world-tour/day1.txt',
            'world-tour/day2.txt',
            'world-tour/day3.txt',
            'world-tour/day4.txt',
            'world-tour/day5.txt',
    ]


@patch('pipeline.notes.fetch_notes.get_table')
@patch('pipeline.notes.fetch_notes.get_latest_day')
def test_unprocessed_notes_none(mock_get_latest_day, mock_get_table):
    mock_get_latest_day.return_value = 5
    mock_get_table.return_value = [
        {'Day': 1}, {'Day': 2}, {'Day': 3}, {'Day': 4}, {'Day': 5}
    ]

    notes = [
        {
            'Key': 'world-tour/day1.txt',
            'LastModified': datetime.datetime(2022, 4, 7, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day2.txt',
            'LastModified': datetime.datetime(2022, 4, 8, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day3.txt',
            'LastModified': datetime.datetime(2022, 4, 9, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day4.txt',
            'LastModified': datetime.datetime(2022, 4, 10, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day5.txt',
            'LastModified': datetime.datetime(2022, 4, 11, 0, 0, 0, tzinfo=tzutc())
        }
    ]

    up_notes = unprocessed_notes(notes, 'trip_name')
    assert up_notes == []


@patch('pipeline.notes.fetch_notes.get_table')
@patch('pipeline.notes.fetch_notes.get_latest_day')
def test_unprocessed_notes_s3_table_mismatch(mock_get_latest_day, mock_get_table):
    mock_get_latest_day.return_value = 5
    mock_get_table.return_value = [
        {'Day': 1}, {'Day': 4}, {'Day': 5}
    ]

    notes = [
        {
            'Key': 'world-tour/day1.txt',
            'LastModified': datetime.datetime(2022, 4, 7, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day2.txt',
            'LastModified': datetime.datetime(2022, 4, 8, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day3.txt',
            'LastModified': datetime.datetime(2022, 4, 9, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day4.txt',
            'LastModified': datetime.datetime(2022, 4, 10, 0, 0, 0, tzinfo=tzutc())
        }, {
            'Key': 'world-tour/day5.txt',
            'LastModified': datetime.datetime(2022, 4, 11, 0, 0, 0, tzinfo=tzutc())
        }
    ]

    up_notes = unprocessed_notes(notes, 'trip_name')
    assert up_notes == ['world-tour/day2.txt', 'world-tour/day3.txt']
