FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

WORKDIR /app

RUN python3 -m venv venv

COPY requirements.txt .
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY ./indexing/ .
COPY ./utils/ .