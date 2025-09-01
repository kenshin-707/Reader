from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

async def parse_thehackernews(html: str, base_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    items = []

    for a in soup.select("a.story-link"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and title:
            items.append({"title": title, "link": urljoin(base_url, href)})

    if not items:  # fallback
        for a in soup.select("article h2 a, h2 a"):
            title = a.get_text(strip=True)
            href = a.get("href")
            if href and title:
                items.append({"title": title, "link": urljoin(base_url, href)})

    # Deduplicate
    seen, deduped = set(), []
    for it in items:
        if it["link"] not in seen:
            seen.add(it["link"])
            deduped.append(it)
    return deduped[:30]

async def parse_fxstreetnews(html: str, base_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    items = []

    # Primary selector
    for article in soup.select("a.story-link"):
        title = article.get_text(strip=True)
        href = article.get("href")
        # Look for content snippet inside parent container
        parent = article.find_parent()
        content = None
        if parent:
            snippet = parent.select_one("p, .excerpt, .summary")
            if snippet:
                content = snippet.get_text(strip=True)
        if href and title:
            items.append({
                "title": title,
                "link": urljoin(base_url, href),
                "content": content or ""
            })

    # Fallback selector
    if not items:
        for a in soup.select("article h2 a, h2 a"):
            title = a.get_text(strip=True)
            href = a.get("href")
            parent = a.find_parent("article")
            content = None
            if parent:
                snippet = parent.select_one("p, .excerpt, .summary")
                if snippet:
                    content = snippet.get_text(strip=True)
            if href and title:
                items.append({
                    "title": title,
                    "link": urljoin(base_url, href),
                    "content": content or ""
                })

    # Deduplicate
    seen, deduped = set(), []
    for it in items:
        if it["link"] not in seen:
            seen.add(it["link"])
            deduped.append(it)

    return deduped[:30]

async def parse_cybersecuritynews(html: str, base_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    items = []
    for sel in ["h2.entry-title a", "h3.entry-title a", "article h2 a", "article h3 a"]:
        for a in soup.select(sel):
            title = a.get_text(strip=True)
            href = a.get("href")
            if href and title:
                items.append({"title": title, "link": urljoin(base_url, href)})
        if items:
            break
    return items[:30]

async def parse_generic_headlines(html: str, base_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    domain = urlparse(base_url).netloc.lower()
    items = []
    for a in soup.select("h1 a, h2 a, h3 a"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and title:
            link = urljoin(base_url, href)
            if urlparse(link).netloc.lower().endswith(domain):
                items.append({"title": title, "link": link})
    return items[:30]

# Registry
SITE_REGISTRY = {
    "1": {"name": "The Hacker News", "url": "https://thehackernews.com/", "parser": parse_thehackernews},
    "2": {"name": "CyberSecurityNews", "url": "https://cybersecuritynews.com/", "parser": parse_cybersecuritynews},
}
