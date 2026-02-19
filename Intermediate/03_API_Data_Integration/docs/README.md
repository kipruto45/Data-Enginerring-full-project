# 03_API_Data_Integration

**Real-time API Data Consumption and Normalization**

Demonstrates:
- HTTP requests with retries and backoff
- Pagination handling
- Rate limiting
- Data normalization to common schema
- Error handling and validation

## Quick Start

1. Fetch data from public API:
```bash
python code/api_etl.py --api https://jsonplaceholder.typicode.com/posts --output results/api_data.csv
```

2. With custom options:
```bash
python code/api_etl.py \
  --api https://jsonplaceholder.typicode.com/posts \
  --batch-size 10 \
  --max-retries 3 \
  --timeout 10
```

## Features

**Resilience:**
- Exponential backoff on failures
- Configurable max retries
- Request timeouts
- Rate limiting (100ms between requests)

**Data Handling:**
- Automatic pagination traversal
- Normalize API responses to consistent schema
- Field extraction and validation
- Metadata tracking (source, fetch time)

**Logging:**
- Structured logging at each stage
- Progress tracking per page
- Error details and retry attempts

## Example: Integrating with Different APIs

```python
# JSONPlaceholder (free test API)
python code/api_etl.py --api https://jsonplaceholder.typicode.com/posts

# Real APIs (example structure):
# python code/api_etl.py --api https://api.github.com/search/repositories
```

## CLI Options

- `--api`: API endpoint URL
- `--output`: Output CSV path
- `--max-retries`: Retry attempts on failure
- `--timeout`: Request timeout (seconds)
- `--batch-size`: Items per API page
- `--log-level`: Logging level

## Production Tips

- Use API keys from environment variables
- Implement rate limiting based on API tier
- Add circuit breakers for cascading failures
- Cache responses when appropriate
- Monitor API health and quota usage
