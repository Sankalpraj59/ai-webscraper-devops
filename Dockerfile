FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y wget unzip gnupg curl chromium chromium-driver && \
    apt-get clean

ENV PYTHONUNBUFFERED=1
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /app
COPY app/ .
COPY .env .env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "updated-web-scraper.py", "--server.port=8501", "--server.address=0.0.0.0"]
