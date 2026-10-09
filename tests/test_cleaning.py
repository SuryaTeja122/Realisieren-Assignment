from processing.cleaning import clean_price, clean_rating, clean_text, clean_tags, normalize_url

def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("10.00") == 10.0
    assert clean_price(None) is None

def test_clean_rating():
    assert clean_rating("star-rating Three") == 3
    assert clean_rating("One") == 1
    assert clean_rating(None) is None

def test_clean_text():
    assert clean_text(" Hello \n World ") == "Hello World"
    assert clean_text("\xa0Test\xa0") == "Test"
    assert clean_text("") is None

def test_clean_tags():
    assert clean_tags(["Z", " a "]) == "a;z"
    assert clean_tags([]) is None

def test_normalize_url():
    assert normalize_url("http://example.com") == "http://example.com"
    assert normalize_url("invalid") is None
