# 03_API_Data_Integration

Resilient API ingestion pipeline with retry handling, pagination, normalization, and CSV export.

## Capabilities

- Configurable endpoint, timeout, and retry policy
- Page-by-page fetch using `_page` and `_limit`
- Response normalization into a stable schema
- Logging for fetch progress and validation behavior

## Quick Start

```bash
pip install -r requirements.txt
python code/api_etl.py \
  --api https://jsonplaceholder.typicode.com/posts \
  --output results/api_data.csv \
  --batch-size 10
```

## Testing

```bash
pytest -q tests
```

Detailed usage and architecture notes are in `docs/README.md`.
