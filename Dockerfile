FROM python:3.8

WORKDIR /travel

COPY requirements.txt requirements.txt

RUN apt-get -y update \
    && pip install -r requirements.txt

COPY . .

RUN pip install .

ENTRYPOINT [ "./entrypoint.sh"]
