import logging

from .disect import parse
from .fetch_notes import get_note
from .fetch_notes import list_notes
from .fetch_notes import unprocessed_notes
from .nlp import process
from .geo_code import geo_code
from .load import put_log

log = logging.getLogger(__name__)


def process_notes(prefix_trip_name, full_trip_name, process_all=False):
    log.info(f'Processing notes for: {prefix_trip_name}')
    notes = list_notes(prefix_trip_name)
    un = unprocessed_notes(notes, full_trip_name, process_all)

    for n in un:
        note_body = get_note(n)
        parsed_note = parse(note_body)
        start_location = geo_code(parsed_note['from_locality'])
        end_location = geo_code(parsed_note['to_locality'])
        nlp_output = process(parsed_note['body'])
        processed_log = {
            'trip_name': full_trip_name,
            'date': parsed_note['date'],
            'day': parsed_note['day'],
            'start_loc': parsed_note['from_locality'],
            'start_lat': start_location['latitude'],
            'start_lng': start_location['longitude'],
            'start_city': start_location['city'],
            'start_state': start_location['state'],
            'start_country': start_location['country'],
            'start_country_code': start_location['country_code'],
            'end_loc': parsed_note['to_locality'],
            'end_lat': end_location['latitude'],
            'end_lng': end_location['longitude'],
            'end_city': end_location['city'],
            'end_state': end_location['state'],
            'end_country': end_location['country'],
            'end_country_code': end_location['country_code'],
            'word_count': nlp_output['word_count'],
            'character_count': nlp_output['char_count'],
            'sentence_count': nlp_output['sent_count'],
            'sentiment': nlp_output['sentiment'],
        }
        log.info(f"Sucessfully processed day {processed_log['day']}")
        put_log(processed_log)
