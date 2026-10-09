# Multi-Source Web Scraping & Data Consolidation

## Overview
This project is a Python-based web scraping and data-processing pipeline that collects information from "Books to Scrape" and "Quotes to Scrape", cleans, validates, deduplicates, and produces a single consolidated dataset.

## Setup & Requirements
- **Python version**: Python 3.10+
- **Dependencies**: `requests`, `beautifulsoup4`, `lxml`, `pytest`

### Installation
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
3. Install dependencies: `pip install -r requirements.txt`

### How to Run
Run the main pipeline:
```bash
python main.py
```
This will generate `output/final_dataset.csv`, `output/summary_report.json`, and write logs to `logs/scraper.log`.

To run tests:
```bash
pytest tests/
```

## Architecture
- **Pagination**: The scraper extracts the "next" link from the HTML (`li.next > a`), joins it with the base URL, and iterates until no next link is found.
- **Data Model**: The common dataset includes `source`, `source_url`, `name_or_title`, `category`, `price`, `rating`, `author`, `tags`, `description`, `scraped_at`.
- **Cleaning**: Trims spaces, removes non-breaking spaces (`\xa0`), converts price to float, converts rating words ("Three") to integers, lowercases and sorts tags.
- **Validation**: Rejects records if the source is unknown, name/title is empty, URL is missing/invalid, price is negative, or rating is outside 1-5.
- **Deduplication**: Uses a SHA-256 fingerprint generated from lowercase, space-stripped, punctuation-free combinations of source + title (for books) and source + author + title[:50] (for quotes).
- **Error Handling**: Implements `requests` retry adapters (for HTTP 429, 500+). Each scraper function wraps record parsing in try/except blocks to skip bad records, and logs errors without stopping the run.
- **Assumptions**: Missing data fields (e.g. price for quotes) are mapped to empty/None.
- **Known Limitations**: The Book scraper does not visit detail pages, so `category` and `description` are left empty to reduce request overhead.
- **AI Usage Summary**: AI was used to bootstrap the script structure and write boilerplate. Please see `AI_USAGE.md` for details.
