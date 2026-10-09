import logging
import csv
import json
from pathlib import Path
import time

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes
from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import find_duplicates

def setup_logging():
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/scraper.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def main():
    start_time = time.time()
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting scraper pipeline")
    
    raw_records = []
    
    try:
        books = scrape_books()
        raw_records.extend(books)
    except Exception as e:
        logger.error("Books scraper failed entirely: %s", e)
        books = []
        
    try:
        quotes = scrape_quotes()
        raw_records.extend(quotes)
    except Exception as e:
        logger.error("Quotes scraper failed entirely: %s", e)
        quotes = []
        
    stats = {
        "collected_per_source": {
            "Books to Scrape": len(books),
            "Quotes to Scrape": len(quotes)
        },
        "records_after_cleaning": {
            "Books to Scrape": 0,
            "Quotes to Scrape": 0
        },
        "rejected_by_reason": {},
        "duplicates_detected": 0,
        "final_record_count": 0,
        "duration_seconds": 0.0
    }
    
    valid_records = []
    for raw in raw_records:
        source = raw.get("source")
        try:
            cleaned = clean_record(raw)
            stats["records_after_cleaning"][source] = stats["records_after_cleaning"].get(source, 0) + 1
            
            problems = validate_record(cleaned)
            if not problems:
                valid_records.append(cleaned)
            else:
                logger.warning("Rejected record from %s: %s (Reasons: %s)", source, cleaned.get("source_url"), problems)
                for p in problems:
                    stats["rejected_by_reason"][p] = stats["rejected_by_reason"].get(p, 0) + 1
                    
        except Exception as e:
            logger.error("Failed to clean/validate record: %s", e)
            stats["rejected_by_reason"]["processing_error"] = stats["rejected_by_reason"].get("processing_error", 0) + 1
            
    unique_records, duplicate_records = find_duplicates(valid_records)
    stats["duplicates_detected"] = len(duplicate_records)
    stats["final_record_count"] = len(unique_records)
    
    for d in duplicate_records:
        logger.info("Duplicate found: %s", d.get("name_or_title"))
        
    Path("output").mkdir(exist_ok=True)
    
    if unique_records:
        fieldnames = [
            "source", "source_url", "name_or_title", "category", "price", 
            "rating", "author", "tags", "description", "scraped_at"
        ]
        with open("output/final_dataset.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in unique_records:
                row = {k: r.get(k) for k in fieldnames}
                writer.writerow(row)
                
    stats["duration_seconds"] = round(time.time() - start_time, 2)
    
    with open("output/summary_report.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)
        
    logger.info("Pipeline completed. Final records: %d", len(unique_records))

if __name__ == "__main__":
    main()
