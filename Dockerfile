FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY . /workspace

# Install all unique dependencies declared across project requirements files.
RUN set -eux; \
    python -m pip install --upgrade pip; \
    find . -type f -name requirements.txt -print0 \
      | xargs -0 -I{} sh -c 'grep -Ehv "^[[:space:]]*(#|$)" "{}" || true' \
      | sort -u > /tmp/requirements-all.txt; \
    if [ -s /tmp/requirements-all.txt ]; then pip install -r /tmp/requirements-all.txt; fi

CMD ["bash"]
