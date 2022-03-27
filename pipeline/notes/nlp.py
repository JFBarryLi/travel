import re
import logging

import nltk

nltk.download('punkt')

log = logging.getLogger(__name__)


def process(body):
    num_words = word_count(body)
    num_chars = char_count(body)
    num_sent = sent_count(body)

    output = {
        'word_count': num_words,
        'char_count': num_chars,
        'sent_count': num_sent,
    }

    return output


def word_count(body):
    try:
        count = len(re.findall(r'\w+', body))
        return count
    except Exception as e:
        log.error(f'Failed to count words from body. Exception: {e}.')


def char_count(body):
    try:
        count = len(body)
        return count
    except Exception as e:
        log.error(f'Failed to count characters from body. Exception: {e}.')


def sent_count(body):
    try:
        count = len(nltk.sent_tokenize(body))
        return count
    except Exception as e:
        log.error(f'Failed to count sentences from body. Exception: {e}.')
