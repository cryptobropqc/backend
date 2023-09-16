FROM python:3.10.13

COPY ./CryptoBro /srv/www/CryptoBro
WORKDIR /srv/www/CryptoBro

RUN pip install -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate