# pull official base image
FROM python:3.7.10-slim-buster

# set working directory
COPY . /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install ffmpeg libavcodec-extra

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt