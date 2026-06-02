# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

ARG BUILD_VERSION=0.2.0

LABEL org.opencontainers.image.title="CV Extractor" \
      org.opencontainers.image.description="Extract name, email, and phone from PDF/DOCX resumes" \
      org.opencontainers.image.version=${BUILD_VERSION} \
      org.opencontainers.image.licenses=MIT

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
       gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

ARG BUILD_VERSION=0.2.0
ARG BUILD_DATE
ARG COMMIT_SHA

LABEL org.opencontainers.image.title="CV Extractor" \
      org.opencontainers.image.description="Extract name, email, and phone from PDF/DOCX resumes" \
      org.opencontainers.image.version=${BUILD_VERSION} \
      org.opencontainers.image.created=${BUILD_DATE} \
      org.opencontainers.image.revision=${COMMIT_SHA} \
      org.opencontainers.image.source="https://github.com/instax-dutta/CvExtractor-Webapp" \
      org.opencontainers.image.licenses=MIT

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

RUN mkdir -p uploads && chown -R appuser:appuser /app

EXPOSE 8000

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
