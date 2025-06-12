FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /minus_lviv

WORKDIR /minus_lviv

COPY web/requirements.txt /minus_lviv/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /minus_lviv/
