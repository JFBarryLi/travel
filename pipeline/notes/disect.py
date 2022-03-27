import logging
import re

log = logging.getLogger(__name__)


def parse(txt):
    day = parse_day(txt)
    from_locality = None
    to_locality = None
    date = None
    body = None

    disected = {
        'day': day,
        'from_locality': from_locality,
        'to_locality': to_locality,
        'date': date,
        'body': body,
    }

    return disected


def parse_day(txt):
    try:
        day = re.sub('[a-zA-Z]', '', txt.split('\n')[0].replace(' ', ''))
        return int(day)
    except Exception as e:
        log.error(f'Failed to parse day from text. Exception: {e}')
