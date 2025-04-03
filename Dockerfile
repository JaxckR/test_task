FROM python:3.12-slim
RUN groupadd -r groupadmin && useradd -r -g groupadmin admin

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip

WORKDIR cafe/

COPY requirements.txt .
RUN pip install -r requirments.txt

COPY . .

RUN chmod -R 777 *

WORKDIR cafe/src

EXPOSE 8000

USER admin