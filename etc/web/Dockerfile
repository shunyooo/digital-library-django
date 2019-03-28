FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
RUN sed -i '/jessie-updates/d' /etc/apt/sources.list
RUN apt-get update && apt-get -y install poppler-utils python-poppler
ADD . /app/