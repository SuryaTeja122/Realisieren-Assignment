import re
from datetime import datetime, timezone

RATING_MAP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

def clean_text(value):
    if value is None:
        return None
    text = " ".join(value.replace("\xa0", " ").split())
    return text or None

def strip_quotes(value):
    if not value:
        return None
    val = value.strip('“”"\'')
    return val

def clean_price(raw):
    if not raw:
        return None
    match = re.search(r"\d+(?:\.\d+)?", raw.replace(",", ""))
    return float(match.group()) if match else None

def clean_rating(raw):
    for word in (raw or "").lower().split():
        if word in RATING_MAP:
            return RATING_MAP[word]
    return None

def clean_tags(tags_list):
    if not tags_list:
        return None
    cleaned = sorted([clean_text(t).lower() for t in tags_list if clean_text(t)])
    return ";".join(cleaned) if cleaned else None

def normalize_url(url):
    if not url:
        return None
    url = clean_text(url)
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return None

def clean_record(raw_rec):
    rec = {
        "source": clean_text(raw_rec.get("source")),
        "source_url": normalize_url(raw_rec.get("source_url")),
        "name_or_title": clean_text(raw_rec.get("name_or_title")),
        "category": clean_text(raw_rec.get("category")),
        "price": clean_price(raw_rec.get("price_raw")),
        "rating": clean_rating(raw_rec.get("rating_raw")),
        "author": clean_text(raw_rec.get("author")),
        "tags": clean_tags(raw_rec.get("tags_raw")) if isinstance(raw_rec.get("tags_raw"), list) else None,
        "description": clean_text(raw_rec.get("description")),
        "scraped_at": datetime.now(timezone.utc).isoformat()
    }
    
    if rec["source"] == "Quotes to Scrape":
        rec["name_or_title"] = strip_quotes(rec["name_or_title"])
        
    return rec
