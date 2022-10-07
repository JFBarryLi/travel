import re
import logging
from decimal import Decimal

import nltk
from transformers import (
    RobertaTokenizerFast,
    TFRobertaForSequenceClassification,
    pipeline,
)

nltk.download('punkt')

tokenizer = RobertaTokenizerFast.from_pretrained(
    "arpanghoshal/EmoRoBERTa"
)
model = TFRobertaForSequenceClassification.from_pretrained(
    "arpanghoshal/EmoRoBERTa"
)
emotion = pipeline(
    'sentiment-analysis',
    model='arpanghoshal/EmoRoBERTa',
    return_all_scores=False,
)

log = logging.getLogger(__name__)

EMOJI_MAP = {
    'admiration': '😲',
    'amusement': '😂',
    'anger': '😡',
    'annoyance': '🙄',
    'approval': '👍',
    'caring': '🤗',
    'confusion': '😕',
    'curiosity': '🤔',
    'desire': '😍',
    'disappointment': '😞',
    'disapproval': '👎',
    'disgust': '🤮',
    'embarrassment': '😳',
    'excitement': '🤩',
    'fear': '😨',
    'gratitude': '🙏',
    'grief': '😢',
    'joy': '😃',
    'love': '❤️',
    'nervousness': '😬',
    'optimism': '🌞',
    'pride': '😌',
    'realization': '💡',
    'relief': '😅',
    'remorse': '😔',
    'sadness': '😞',
    'surprise': '😲',
    'neutral': '😐',
}


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
        result = []
        paragraphs = body.split('\n\n')
        for paragraph in paragraphs:
            emotion_labels = emotion(paragraph)
            emotion_labels.sort(key=lambda i: i['score'], reverse=True)
            para_sentiment = emotion_labels

            for item in para_sentiment:
                item['emoji'] = EMOJI_MAP[item['label']]
                item['score'] = Decimal(item['score'])

            result.append(para_sentiment[0])

        log.info(f'Successfully predicted sentiment: {result}')
        return result
    except Exception as e:
        log.error(f'Failed to predict sentiment from body. Exception: {e}.')
