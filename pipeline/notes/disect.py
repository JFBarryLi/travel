import logging
import re

log = logging.getLogger(__name__)


def parse(txt):
    day = parse_day(txt)
    locality = parse_locality(txt)
    from_locality = locality['from_locality']
    to_locality = locality['to_locality']
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


def parse_locality(txt):
    try:
        line = txt.split('\n')[1].split('-')

        # Handle cases where '-' is in the locality's name
        if len(line) > 2:
            locality = '-'.join(line[:-1]).strip()
        else:
            locality = line[0].strip()

        if '/' in locality:
            loc_split = locality.split('/')
            from_locality = loc_split[0]
            to_locality = loc_split[1]
        else:
            from_locality = locality
            to_locality = locality

        return {'from_locality': from_locality, 'to_locality': to_locality}
    except Exception as e:
        log.error(f'Failed to parse locality from text. Exception: {e}')
