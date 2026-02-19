"""Twitter/Reddit Social Media Data Pipeline

Demonstrates:
- Social media API integration
- Text preprocessing (lowercasing, tokenization, stop word removal)
- Sentiment analysis preparation
- Deduplication handling
- Streaming vs batch processing patterns
"""

import csv
import logging
import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
import random

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "raw" / "social_posts.csv"
DEFAULT_OUTPUT = ROOT / "results" / "social_summary.csv"


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("social_etl")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def parse_args():
    p = argparse.ArgumentParser(description="Social Media Data Pipeline")
    p.add_argument("--input", default=str(DEFAULT_DATA), help="Input CSV path")
    p.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output CSV path")
    p.add_argument("--generate", action="store_true", help="Generate sample data")
    p.add_argument("--samples", type=int, default=5000, help="Sample size")
    p.add_argument("--min-length", type=int, default=10, help="Min post length (chars)")
    p.add_argument("--log-level", default="INFO", help="Logging level")
    return p.parse_args()


def generate_social_data(csv_path, num_posts=5000, logger=None):
    """Generate simulated social media posts"""
    sample_texts = [
        "Just launched our new product! Really excited about this #tech #startup",
        "Data engineering is hard but worth it #datascience #learning",
        "Building scalable systems with Python and PostgreSQL",
        "Love working with ETL pipelines, optimizing performance",
        "The future of data is real-time streaming #BigData",
        "Machine learning models are getting better every day",
        "Cloud computing has changed how we build applications",
        "Open source is amazing, contributing to the community",
        "Working on a cool NLP project with transformers",
        "Data visualization with modern dashboards",
    ]
    
    platforms = ["twitter", "reddit"]
    
    rows = []
    for i in range(num_posts):
        post_text = random.choice(sample_texts)
        if random.random() > 0.8:  # Add some variation
            post_text += f" {random.choice(['Amazing!', 'So cool!', 'Great content!', 'Very informative'])}"
        
        rows.append({
            "post_id": f"post_{i+1}",
            "platform": random.choice(platforms),
            "author": f"user_{random.randint(1, 500)}",
            "text": post_text,
            "likes": random.randint(0, 10000),
            "shares": random.randint(0, 1000),
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
        })
    
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    if logger:
        logger.info(f"Generated {num_posts} social posts to {csv_path}")


def preprocess_text(text, logger=None):
    """Preprocess text for NLP analysis"""
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove special characters but keep hashtags and mentions
    text = re.sub(r'[^a-z0-9\s#@]', '', text)
    
    # Tokenize (simple split)
    tokens = text.split()
    
    # Remove stop words (simple list)
    stop_words = {"the", "a", "an", "is", "are", "and", "or", "but", "in", "on", "at", "to", "for"}
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
    
    return tokens


def extract_features(post, logger=None):
    """Extract features from social post for analysis"""
    tokens = preprocess_text(post["text"])
    
    # Extract hashtags and mentions
    hashtags = [t for t in tokens if t.startswith("#")]
    mentions = [t for t in tokens if t.startswith("@")]
    
    # Engagement metrics
    total_engagement = post["likes"] + post["shares"]
    
    # Sentiment indicators (simple keyword matching)
    positive_words = {"amazing", "great", "love", "awesome", "cool", "excellent", "good"}
    negative_words = {"bad", "hate", "worst", "terrible", "poor", "awful"}
    
    sentiment_score = 0
    for token in tokens:
        if token in positive_words:
            sentiment_score += 1
        elif token in negative_words:
            sentiment_score -= 1
    
    return {
        "post_id": post["post_id"],
        "platform": post["platform"],
        "author": post["author"],
        "created_at": post["created_at"],
        "tokens_count": len(tokens),
        "hashtags_count": len(hashtags),
        "mentions_count": len(mentions),
        "likes": post["likes"],
        "shares": post["shares"],
        "total_engagement": total_engagement,
        "sentiment_score": sentiment_score,
        "top_hashtags": ",".join(hashtags[:3]) if hashtags else "",
        "processed_at": datetime.now().isoformat()
    }


def load_and_process(input_path, output_path, min_length=10, logger=None):
    """Load, process, and save social data"""
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    processed_posts = []
    duplicate_ids = set()
    
    # Read and process
    with input_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Deduplication
            if row["post_id"] in duplicate_ids:
                if logger:
                    logger.debug(f"Skipping duplicate: {row['post_id']}")
                continue
            duplicate_ids.add(row["post_id"])
            
            # Filter by text length
            if len(row["text"]) < min_length:
                continue
            
            # Parse numeric fields
            row["likes"] = int(row["likes"])
            row["shares"] = int(row["shares"])
            
            # Extract features
            features = extract_features(row, logger)
            processed_posts.append(features)
    
    # Save processed data
    if processed_posts:
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=processed_posts[0].keys())
            writer.writeheader()
            writer.writerows(processed_posts)
        
        if logger:
            logger.info(f"Processed {len(processed_posts)} posts, saved to {output_path}")
            # Log summary stats
            avg_engagement = sum(p["total_engagement"] for p in processed_posts) / len(processed_posts)
            avg_sentiment = sum(p["sentiment_score"] for p in processed_posts) / len(processed_posts)
            logger.info(f"Summary: avg_engagement={avg_engagement:.1f}, avg_sentiment={avg_sentiment:.2f}")
    else:
        if logger:
            logger.warning("No posts to process")
    
    return len(processed_posts)


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger(getattr(logging, args.log_level.upper(), logging.INFO))
    
    input_path = Path(args.input)
    
    if args.generate:
        generate_social_data(input_path, num_posts=args.samples, logger=logger)
    
    if input_path.exists():
        count = load_and_process(input_path, args.output, min_length=args.min_length, logger=logger)
        logger.info(f"Social media ETL complete: {count} posts processed")
    else:
        logger.error(f"Input file not found: {input_path}")
        raise SystemExit(1)
