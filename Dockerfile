FROM python:3.8

WORKDIR /travel

COPY requirements.txt requirements.txt

RUN apt-get -y update \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir .

ENTRYPOINT [ "./entrypoint.sh"]
