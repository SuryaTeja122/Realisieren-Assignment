from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging
from .base_scraper import create_session
import time

logger = logging.getLogger(__name__)

def parse_quote(div, page_url):
    text = div.select_one("span.text")
    author = div.select_one("small.author")
    tags = div.select("a.tag")
    about_link = div.select_one("a[href^='/author/']")
    
    return {
        "source": "Quotes to Scrape",
        "source_url": urljoin(page_url, about_link["href"]) if about_link else None,
        "name_or_title": text.get_text() if text else None,
        "category": "Quotes",
        "price_raw": None,
        "rating_raw": None,
        "author": author.get_text() if author else None,
        "tags_raw": [t.get_text() for t in tags] if tags else None,
        "description": None,
    }

def scrape_quotes():
    session = create_session()
    url = "https://quotes.toscrape.com/"
    page = 1
    records = []
    
    while url:
        logger.info("Quotes to Scrape - Page %d: %s", page, url)
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
        except Exception as exc:
            logger.error("Failed to fetch Quotes to Scrape %s: %s", url, exc)
            break
            
        soup = BeautifulSoup(response.text, "lxml")
        
        for quote_div in soup.select("div.quote"):
            try:
                records.append(parse_quote(quote_div, url))
            except Exception as e:
                logger.warning("Failed to parse a quote on %s: %s", url, e)
                
        next_link = soup.select_one("li.next > a")
        url = urljoin(url, next_link["href"]) if next_link else None
        page += 1
        time.sleep(0.5)
        
    return records
