import logging

from .disect import parse
from .fetch_notes import get_note
from .fetch_notes import list_notes
from .fetch_notes import unprocessed_notes
from .nlp import process

log = logging.getLogger(__name__)


def process_notes(prefix_trip_name, full_trip_name):
    log.info(f'Processing notes for: {prefix_trip_name}')
    notes = list_notes(prefix_trip_name)
    un = unprocessed_notes(notes, full_trip_name)

    for n in un:
        note_body = get_note(n)
        parsed_note = parse(note_body)
        nlp_output = process(parsed_note['body'])
        processed_log = {
            'trip_name': full_trip_name,
            'date': parsed_note['date'],
            'day': parsed_note['day'],
            'start_loc': parsed_note['from_locality'],
            'start_lat': '',
            'start_lng': '',
            'end_loc': parsed_note['to_locality'],
            'end_lat': '',
            'end_lng': '',
            'word_count': nlp_output['word_count'],
            'character_count': nlp_output['char_count'],
            'sentence_count': nlp_output['sent_count'],
            'sentiment': nlp_output['sentiment'],
        }
