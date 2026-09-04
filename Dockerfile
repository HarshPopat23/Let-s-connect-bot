FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --upgrade pip && pip install .

COPY knowledge ./knowledge
COPY scripts ./scripts
COPY docs ./docs
RUN mkdir -p /app/data \
    && chown -R 65532:65532 /app/data \
    && chmod +x /app/scripts/*.sh

USER 65532:65532

CMD ["ollm"]
