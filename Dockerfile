FROM python:2.7

ENV PYTHONPATH=/app

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD ./ /app

WORKDIR /app
