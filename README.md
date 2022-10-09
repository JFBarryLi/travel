![Deploy](https://github.com/JFBarryLi/travel/actions/workflows/ci.yml/badge.svg)

# Travel

## Setup
Setup the following environment variables.
```bash
export ALERT_WEBHOOK="Discord webhook url for logging."
export NOTES_BUCKET_NAME="Bucket storing the notes."
export TRAVEL_TABLE="Name of the DynamoDB table to stored output."
```

## Local Development

```bash
git clone https://github.com/JFBarryLi/travel.git
python -m venv venv
. venv/bin/activate
pip install -e .
```

### Testing
```bash
pytest -vv
```

## Build

```bash
docker build -t travel .
```

## Usage

### To run the entire pipeline
```bash
./scripts/notes_pipeline
```

### nlp
```python
from pipeline.notes.nlp import process

text = 'This is an example text.'

process(text)
```

BERT base sentiment analysis trained on the GoEmotions dataset - arpanghoshal/EmoRoBERTa

```python
from pipeline.notes.nlp import predict_sentiment

text = 'This is an example text.'

predict_sentiment(text)

```

### geo coding
```python
from pipeline.notes.geo_code import geo_code

geo_code('Lisbon')
```

### To deal with ambiguous geo-coding
First update `geo_code_overrides.py`

Then run:
```bash
./scripts/geo_code_overrides.py
```

## Expected format for journal entries
```
Day 123
City_name - Thursday, February 10, 2022

Body of text. Body of text. Body of text.
Body of text.

Body of text. Body of text.
```

## License
See [LICENSE](./LICENSE) for more information.
