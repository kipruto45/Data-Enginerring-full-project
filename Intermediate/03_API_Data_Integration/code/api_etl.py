"""API Data Integration ETL

Demonstrates:
- HTTP requests with retries
- Pagination handling
- Rate limiting and backoff
- Data normalization from API responses
- Error handling and validation
"""

import requests
import logging
import time
import argparse
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "results" / "api_data.csv"


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("api_etl")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def parse_args():
    p = argparse.ArgumentParser(description="API Data Integration")
    p.add_argument("--api", default="https://jsonplaceholder.typicode.com/posts", help="API endpoint")
    p.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output CSV path")
    p.add_argument("--max-retries", type=int, default=3, help="Max retries on failure")
    p.add_argument("--timeout", type=int, default=10, help="Request timeout (seconds)")
    p.add_argument("--batch-size", type=int, default=10, help="Items per page")
    p.add_argument("--log-level", default="INFO", help="Logging level")
    return p.parse_args()


def fetch_with_retries(url, max_retries=3, timeout=10, logger=None):
    """Fetch data from API with exponential backoff"""
    for attempt in range(max_retries):
        try:
            if logger:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # exponential backoff
                if logger:
                    logger.warning(f"Request failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                if logger:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                raise


def fetch_paginated_data(base_url, batch_size=10, max_retries=3, timeout=10, logger=None):
    """Fetch all pages from a paginated API"""
    all_data = []
    page = 1
    
    while True:
        url = f"{base_url}?_page={page}&_limit={batch_size}"
        try:
            data = fetch_with_retries(url, max_retries=max_retries, timeout=timeout, logger=logger)
            if not data:
                break  # No more data
            all_data.extend(data)
            if logger:
                logger.info(f"Fetched page {page}: {len(data)} items (total: {len(all_data)})")
            page += 1
            time.sleep(0.1)  # Rate limiting: 100ms between requests
        except Exception as e:
            if logger:
                logger.error(f"Error fetching page {page}: {e}")
            break
    
    return all_data


def normalize_data(raw_data, logger=None):
    """Normalize API response to common schema"""
    normalized = []
    for item in raw_data:
        # Extract relevant fields and add metadata
        record = {
            "id": item.get("id"),
            "title": item.get("title", ""),
            "content": item.get("body", ""),
            "user_id": item.get("userId"),
            "api_source": "jsonplaceholder",
            "fetched_at": datetime.now().isoformat(),
            "valid": True
        }
        
        # Validation: check required fields
        if not record["id"] or not record["title"]:
            record["valid"] = False
            if logger:
                logger.warning(f"Invalid record: {record['id']}")
        
        normalized.append(record)
    
    if logger:
        logger.info(f"Normalized {len(normalized)} records")
    
    return normalized


def save_to_csv(data, output_path, logger=None):
    """Save normalized data to CSV"""
    import csv
    
    if not data:
        if logger:
            logger.warning("No data to save")
        return 0
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    if logger:
        logger.info(f"Saved {len(data)} records to {output_path}")
    
    return len(data)


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger(getattr(logging, args.log_level.upper(), logging.INFO))
    
    try:
        logger.info(f"Starting API ETL from {args.api}")
        
        # Fetch paginated data
        raw_data = fetch_paginated_data(
            args.api,
            batch_size=args.batch_size,
            max_retries=args.max_retries,
            timeout=args.timeout,
            logger=logger
        )
        
        if raw_data:
            # Normalize data
            normalized = normalize_data(raw_data, logger=logger)
            
            # Save to CSV
            count = save_to_csv(normalized, args.output, logger=logger)
            logger.info(f"API ETL complete: {count} records processed")
        else:
            logger.warning("No data fetched from API")
    
    except Exception as e:
        logger.exception("API ETL failed")
        raise SystemExit(1)
