# 05_Twitter_Reddit_Data_Pipeline

**Social Media Data Pipeline with NLP Preprocessing**

Demonstrates:
- Text preprocessing (lowercasing, tokenization, stop-word removal)
- Feature extraction (hashtags, mentions, sentiment indicators)
- Deduplication handling
- Engagement metrics calculation
- Sentiment analysis preparation

## Quick Start

1. Generate sample social media posts:
```bash
python code/social_pipeline.py --generate --samples 5000
```

2. Process and extract features:
```bash
python code/social_pipeline.py --input data/raw/social_posts.csv --output results/social_summary.csv
```

3. View processed data:
```bash
head results/social_summary.csv
```

## Features

**Text Preprocessing:**
- Lowercase normalization
- URL removal
- Special character cleaning
- Tokenization
- Stop-word removal

**Feature Extraction:**
- Token count
- Hashtag extraction and counting
- @mention detection
- Engagement metrics (likes, shares, total)
- Sentiment scoring (keyword-based)
- Top hashtags per post

**Quality Checks:**
- Minimum text length filtering
- Deduplication by post ID
- Timestamp validation

**Output Schema:**
- post_id, platform, author
- tokens_count, hashtags_count, mentions_count
- likes, shares, total_engagement
- sentiment_score, top_hashtags
- processed_at (processing timestamp)

## NLP Pipeline Extensions

This data is prepared for:
- Sentiment analysis (TextBlob, VADER, transformers)
- Topic modeling (LDA, NMF)
- Trend detection (rising hashtags)
- Influencer identification
- Content recommendation systems

## CLI Options

- `--input`: Input CSV path
- `--output`: Output CSV path
- `--generate`: Generate sample posts
- `--samples`: Number of posts to generate
- `--min-length`: Minimum post length (characters)
- `--log-level`: Logging level

## Real-World Integration

```bash
# Streaming from Twitter API (pseudo-code)
# python code/social_pipeline.py --stream twitter --api-key YOUR_KEY

# Batch processing Reddit data
# python code/social_pipeline.py --input reddit_export.csv --output reddit_processed.csv
```

## Advanced Topics

- Real-time streaming with Kafka
- Machine learning model serving
- A/B testing content strategies
- Anomaly detection (spam, bots)
- Multi-lingual support
