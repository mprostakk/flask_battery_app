FROM python:3.8

COPY requirements.txt /

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD python app.py
