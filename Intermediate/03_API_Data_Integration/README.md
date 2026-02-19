# 03_API_Data_Integration

**Real-time API Data Consumption and Normalization**

This project demonstrates robust API data integration with comprehensive error handling, retries, and data normalization.

## Features

- **Resilient HTTP Requests**: Exponential backoff, configurable retries, timeouts
- **Pagination Support**: Automatic handling of paginated APIs
- **Rate Limiting**: Built-in delays between requests
- **Data Normalization**: Consistent schema across different API sources
- **Comprehensive Testing**: Unit tests covering all major functions
- **Error Handling**: Graceful failure handling for network issues, invalid responses
- **Logging**: Structured logging with configurable levels

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with default settings (JSONPlaceholder API)
python code/api_etl.py

# Run with custom settings
python code/api_etl.py \
  --api https://jsonplaceholder.typicode.com/posts \
  --batch-size 5 \
  --max-retries 3 \
  --output results/custom_output.csv \
  --log-level DEBUG
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=code.api_etl
```

## Architecture

- `code/api_etl.py`: Main ETL script with CLI interface
- `tests/test_api_etl.py`: Comprehensive unit tests
- `docs/README.md`: Detailed documentation
- `requirements.txt`: Python dependencies

## Production Considerations

- Add API key management for authenticated endpoints
- Implement circuit breakers for cascading failures
- Add response caching for frequently accessed data
- Monitor API rate limits and quotas
- Set up proper logging aggregation