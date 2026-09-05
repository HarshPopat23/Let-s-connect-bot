FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    VECLIB_MAXIMUM_THREADS=1 \
    NUMEXPR_NUM_THREADS=1 \
    FASTEMBED_THREADS=1 \
    HF_HOME=/app/cache/hf \
    FASTEMBED_CACHE_PATH=/app/cache \
    HF_HUB_DISABLE_SYMLINKS_WARNING=1 \
    HF_HUB_ENABLE_HF_TRANSFER=0

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --upgrade pip && pip install .

# Pre-download FastEmbed model during docker build so it is stored in the image filesystem
# and NEVER downloaded into memory at container runtime (prevents 512MB RAM OOM)
RUN mkdir -p /app/cache \
    && python -c "from fastembed import TextEmbedding; TextEmbedding('BAAI/bge-small-en-v1.5', cache_dir='/app/cache', threads=1)"

COPY knowledge ./knowledge
COPY scripts ./scripts
COPY docs ./docs
RUN mkdir -p /app/data \
    && chown -R 65532:65532 /app/data /app/cache \
    && chmod +x /app/scripts/*.sh

USER 65532:65532

CMD ["ollm"]
