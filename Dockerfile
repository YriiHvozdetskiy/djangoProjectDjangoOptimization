FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

# встановлюємо залежності для підключення python до postgresql
RUN apk add postgresql-client build-base postgresql-dev

# -r показуєм з якого файлу потрібно встановити залежності
RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user
