FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         tesseract-ocr \
         libglib2.0-0 libsm6 libxrender1 libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
