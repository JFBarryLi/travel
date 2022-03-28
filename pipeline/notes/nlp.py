import re
import logging

from flair.data import Sentence
from flair.models import TextClassifier
import nltk

classifier = TextClassifier.load('en-sentiment')
nltk.download('punkt')

log = logging.getLogger(__name__)


def process(body):
    num_words = word_count(body)
    num_chars = char_count(body)
    num_sent = sent_count(body)

    sentiment = predict_sentiment(body)

    output = {
        'word_count': num_words,
        'char_count': num_chars,
        'sent_count': num_sent,
        'sentiment': sentiment,
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


def predict_sentiment(body):
    try:
        sentences = nltk.sent_tokenize(body)
        result = {'POSITIVE': 0, 'NEGATIVE': 0}

        for s in sentences:
            sentence = Sentence(s)
            classifier.predict(sentence)
            labels = sentence.get_label_names()
            if 'POSITIVE' in labels:
                result['POSITIVE'] += 1
            elif 'NEGATIVE' in labels:
                result['NEGATIVE'] += 1

        return result
    except Exception as e:
        log.error(f'Failed to predict sentiment from body. Exception: {e}.')
