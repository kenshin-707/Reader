import requests
from bs4 import BeautifulSoup
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# Create session with retries
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)
session.headers.update({"User-Agent": "FlaskNewsScraperBot/1.0"})

SUPPORTED_SITES = {
    "hackernews": "https://news.ycombinator.com/",
    "thehackernews": "https://thehackernews.com/",
    "bleepingcomputer": "https://www.bleepingcomputer.com/",
}

def scrape_articles(site, keyword):
    """Scrapes the selected site for articles containing the keyword."""
    if site not in SUPPORTED_SITES:
        raise ValueError("Unsupported site")

    url = SUPPORTED_SITES[site]
    logger.info(f"Scraping {site} for keyword '{keyword}'")

    try:
        resp = session.get(url, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    if site == "hackernews":
        links = soup.select(".athing .titleline a")
        for link in links:
            title = link.get_text()
            href = link.get("href")
            if keyword.lower() in title.lower():
                results.append({"title": title, "url": href})

    elif site == "thehackernews":
        articles = soup.select(".body-post h2 a")
        for a in articles:
            title = a.get_text()
            href = a.get("href")
            if keyword.lower() in title.lower():
                results.append({"title": title, "url": href})

    elif site == "bleepingcomputer":
        articles = soup.select(".bc_latest_news a")
        for a in articles:
            title = a.get_text().strip()
            href = "https://www.bleepingcomputer.com" + a.get("href")
            if keyword.lower() in title.lower():
                results.append({"title": title, "url": href})

    return results
