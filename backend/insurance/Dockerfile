FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y postgresql-client nginx

RUN pip install django psycopg2-binary djangorestframework djangorestframework-simplejwt django-extensions Werkzeug pyOpenSSL pyotp qrcode pyaml

COPY ./entrypoint.sh /entrypoint.sh
COPY . .

RUN chmod +x /entrypoint.sh

# RUN chmod +x /code/bin/host
# RUN chmod +x /code/bin/verifier

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]