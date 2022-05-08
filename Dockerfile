FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN mkdir /music_meta_web

WORKDIR /music_meta_web

COPY . /music_meta_web/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt