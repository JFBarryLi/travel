from importlib import resources

import pipeline.notes.tests.data as data

examples = {}

for file_name in resources.contents(data):
    if file_name.endswith('.txt'):
        txt = resources.read_text(data, file_name)
        examples[file_name] = txt
