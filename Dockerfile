FROM python:2.7.11

ENV PYTHONBUFFERED 1
ENV APPLICATION_ROOT /stormtrooper/

RUN mkdir -p $APPLICATION_ROOT
WORKDIR $APPLICATION_ROOT
ADD requirements.txt $APPLICATION_ROOT
ADD requirements-dev.txt $APPLICATION_ROOT
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
ADD . $APPLICATION_ROOT
