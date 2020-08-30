FROM python:3.8

RUN mkdir /src
WORKDIR /src
COPY .env config.py database.py handlers.py main.py requirements.txt /src/
RUN pip install -r requirements.txt
