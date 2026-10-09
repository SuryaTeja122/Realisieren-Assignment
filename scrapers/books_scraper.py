from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging
from .base_scraper import create_session
import time

logger = logging.getLogger(__name__)

def parse_book(article, page_url):
    link = article.select_one("h3 > a")
    price = article.select_one("p.price_color")
    rating = article.select_one("p.star-rating")
    return {
        "source": "Books to Scrape",
        "source_url": urljoin(page_url, link["href"]) if link and link.get("href") else None,
        "name_or_title": link.get("title") if link else None,
        "category": None,
        "price_raw": price.get_text() if price else None,
        "rating_raw": " ".join(rating.get("class", [])) if rating else None,
        "author": None,
        "tags_raw": None,
        "description": None,
    }

def scrape_books():
    session = create_session()
    url = "https://books.toscrape.com/"
    page = 1
    records = []
    
    while url:
        logger.info("Books to Scrape - Page %d: %s", page, url)
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
        except Exception as exc:
            logger.error("Failed to fetch Books to Scrape %s: %s", url, exc)
            break
            
        soup = BeautifulSoup(response.text, "lxml")
        
        for article in soup.select("article.product_pod"):
            try:
                records.append(parse_book(article, url))
            except Exception as e:
                logger.warning("Failed to parse a book on %s: %s", url, e)
                
        next_link = soup.select_one("li.next > a")
        url = urljoin(url, next_link["href"]) if next_link else None
        page += 1
        time.sleep(0.5)
        
    return records
