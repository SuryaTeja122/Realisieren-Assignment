from processing.validation import validate_record

def test_valid_record():
    rec = {
        "source": "Books to Scrape",
        "name_or_title": "A Book",
        "source_url": "http://example.com/book",
        "price": 10.0,
        "rating": 5
    }
    assert validate_record(rec) == []

def test_invalid_record():
    rec = {
        "source": "Unknown",
        "name_or_title": "",
        "source_url": "ftp://example",
        "price": -1,
        "rating": 6
    }
    problems = validate_record(rec)
    assert set(problems) == {"unknown_source", "missing_name", "invalid_url", "invalid_price", "invalid_rating"}
