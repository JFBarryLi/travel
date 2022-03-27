import os

examples = {}

for filename in os.listdir('./examples'):
    with open(os.path.join('./examples', filename), 'r') as f:
        txt = f.read()
        examples[filename] = txt
