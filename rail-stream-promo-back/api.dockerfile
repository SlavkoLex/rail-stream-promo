FROM python:3.12.3-slim

WORKDIR /rail-stream-promo-back

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY src/ /rail-stream-promo-back/src

RUN pip install --no-cache-dir -r src/config_assets/requirements.txt

CMD ["python3", "/rail-stream-promo-back/src/main/app/app.py"]


