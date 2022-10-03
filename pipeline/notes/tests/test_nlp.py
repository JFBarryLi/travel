from ..nlp import process, word_count, char_count, sent_count,\
    predict_sentiment

STD_BODY = 'Day1 - Monday, September 5, 2022\nNew York\n\nThis is a standard body of text. It has several sentences, and some punctuations. What am I? That was a simple question. The answer should be simple as well! I am just a body of text.'


def test_process():
    output = process(STD_BODY)
    assert output['word_count'] == 43
    assert output['char_count'] == 226
    assert output['sent_count'] == 6
    assert output['sentiment'][0][0]['label'] == 'neutral'
    assert output['sentiment'][0][1]['label'] == 'realization'
    assert output['sentiment'][0][2]['label'] == 'approval'


def test_word_count():
    count = word_count(STD_BODY)
    assert count == 43


def test_char_count():
    count = char_count(STD_BODY)
    assert count == 226


def test_sent_count():
    count = sent_count(STD_BODY)
    assert count == 6


def test_predict_sentiment():
    result = predict_sentiment(STD_BODY)
    assert result[0][0]['label'] == 'neutral'
    assert result[0][1]['label'] == 'realization'
    assert result[0][2]['label'] == 'approval'
