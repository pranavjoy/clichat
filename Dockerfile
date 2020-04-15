FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN apt-get install -y locales locales-all

WORKDIR /app

ENV LANG C.UTF-8

ENV LC_ALL C.UTF-8

COPY . /app

CMD python3 chat_server.py