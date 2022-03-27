FROM python:3.8

RUN mkdir           /travel
COPY ./             /travel/
COPY entrypoint.sh  /entrypoint.sh

RUN cd /travel \
  && apt-get -y update \
  && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/entrypoint.sh"]
