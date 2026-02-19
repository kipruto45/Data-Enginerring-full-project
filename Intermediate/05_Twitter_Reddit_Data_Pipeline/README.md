# 05_Twitter_Reddit_Data_Pipeline

Social media ETL workflow for preprocessing text, extracting features, and producing analytics-ready summaries.

## What You Learn

- Text normalization and token filtering
- Hashtag and mention extraction
- Engagement and sentiment feature derivation
- Deduplication and minimum-length filtering

## Quick Start

```bash
pip install -r requirements.txt
python code/social_pipeline.py --generate --samples 5000
python code/social_pipeline.py --input data/raw/social_posts.csv --output results/social_summary.csv
```

## Output

- `results/social_summary.csv` with per-post feature columns for downstream analytics.

See detailed operational notes in `docs/README.md`.
