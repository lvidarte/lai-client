FROM python:2.7

ENV PYTHONPATH=/app
ENV EDITOR=/usr/bin/vim.nox

COPY ./requirements.txt /tmp/requirements.txt

RUN apt-get update && \
    apt-get install -y vim.nox && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD ./ /app

WORKDIR /app
