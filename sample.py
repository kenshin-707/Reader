"""
Async Cybersecurity News Scraper
--------------------------------
Framework: asyncio + aiohttp
Parsers: BeautifulSoup (with lxml parser)

What you get:
- Pick sites to scrape (The Hacker News, CyberSecurityNews, or add your own)
- Add custom URLs dynamically at runtime
- Gets latest titles + links
- JSON output to stdout
- Graceful error handling (timeouts, bad URLs, parse fallbacks)

Why async?
- We hit multiple websites at the same time -> way faster than one-by-one
"""

import asyncio
import json
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup


async def parse_thehackernews(html: str, base_url: str) -> list[dict]:
    """
    The Hacker News homepage often marks articles with <a class="story-link">.
    We try that first; if the layout changes, we fall back to generic selectors.
    """
    soup = BeautifulSoup(html, "lxml")
    items: list[dict] = []

    # 1) Preferred selector
    for a in soup.select("a.story-link"):
        title = (a.get_text(strip=True) or "").strip()
        href = a.get("href")
        if not href or not title:
            continue
        link = urljoin(base_url, href)
        items.append({"title": title, "link": link})

    # 2) Fallback: try article > h2 > a
    if not items:
        for a in soup.select("article h2 a, h2 a"):
            title = (a.get_text(strip=True) or "").strip()
            href = a.get("href")
            if not href or not title:
                continue
            link = urljoin(base_url, href)
            items.append({"title": title, "link": link})

    # Deduplicate by link
    seen = set()
    deduped = []
    for it in items:
        if it["link"] in seen:
            continue
        seen.add(it["link"])
        deduped.append(it)

    return deduped[:30]  # keep it tidy


async def parse_cybersecuritynews(html: str, base_url: str) -> list[dict]:
    """
    CyberSecurityNews often uses typical blog structure with titles in h2/h3.
    We try common patterns first, then fall back to generic heading links.
    """
    soup = BeautifulSoup(html, "lxml")
    items: list[dict] = []

    # 1) Common WP patterns
    for sel in [
        "h2.entry-title a",
        "h3.entry-title a",
        "article h2 a",
        "article h3 a",
    ]:
        for a in soup.select(sel):
            title = (a.get_text(strip=True) or "").strip()
            href = a.get("href")
            if not href or not title:
                continue
            link = urljoin(base_url, href)
            items.append({"title": title, "link": link})

        if items:  # if we got some, stop trying further selectors
            break

    # 2) Fallback: any heading link on the page
    if not items:
        for a in soup.select("h1 a, h2 a, h3 a"):
            title = (a.get_text(strip=True) or "").strip()
            href = a.get("href")
            if not href or not title:
                continue
            link = urljoin(base_url, href)
            items.append({"title": title, "link": link})

    # Deduplicate
    seen = set()
    deduped = []
    for it in items:
        if it["link"] in seen:
            continue
        seen.add(it["link"])
        deduped.append(it)

    return deduped[:30]


async def parse_generic_headlines(html: str, base_url: str) -> list[dict]:
    """
    Generic parser for unknown sites:
    - Looks for links in h1/h2/h3
    - Filters to same-domain links when possible
    - Not perfect, but good enough as a plug-and-play fallback
    """
    soup = BeautifulSoup(html, "lxml")
    items = []

    domain = urlparse(base_url).netloc.lower()

    for a in soup.select("h1 a, h2 a, h3 a"):
        title = (a.get_text(strip=True) or "").strip()
        href = a.get("href")
        if not href or not title:
            continue
        link = urljoin(base_url, href)

        # Heuristic: prefer links pointing to same domain (often article pages)
        if urlparse(link).netloc.lower().endswith(domain):
            items.append({"title": title, "link": link})

    # If nothing matched, accept any heading link
    if not items:
        for a in soup.select("h1 a, h2 a, h3 a"):
            title = (a.get_text(strip=True) or "").strip()
            href = a.get("href")
            if not href or not title:
                continue
            link = urljoin(base_url, href)
            items.append({"title": title, "link": link})

    # Deduplicate
    seen = set()
    deduped = []
    for it in items:
        if it["link"] in seen:
            continue
        seen.add(it["link"])
        deduped.append(it)

    return deduped[:30]


SITE_REGISTRY = {
    "1": {
        "name": "The Hacker News",
        "url": "https://thehackernews.com/",
        "parser": parse_thehackernews,
    },
    "2": {
        "name": "CyberSecurityNews",
        "url": "https://cybersecuritynews.com/",
        "parser": parse_cybersecuritynews,
    },
    # You can add more preset sites here later
}


# -----------------------------
# Networking: fetch with retries
# -----------------------------

DEFAULT_HEADERS = {
    # Pretend to be a normal browser; some sites block "default" clients
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

async def fetch_html(session: aiohttp.ClientSession, url: str, *, max_retries: int = 2) -> str | None:
    """
    Download HTML with a short timeout and a couple of retries.
    Returns None if it ultimately fails.
    """
    for attempt in range(max_retries + 1):
        try:
            async with session.get(url, headers=DEFAULT_HEADERS) as resp:
                # Ensure 2xx OK
                if resp.status != 200:
                    raise aiohttp.ClientResponseError(
                        request_info=resp.request_info,
                        history=resp.history,
                        status=resp.status,
                        message=f"HTTP {resp.status}",
                        headers=resp.headers,
                    )
                return await resp.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if attempt < max_retries:
                await asyncio.sleep(0.5 * (2 ** attempt))  # exponential backoff
            else:
                # Log-style print; we keep going for other sites
                print(f"Warning: failed to fetch {url}: {e}")
                return None


# -----------------------------
# Orchestration: one site scrape
# -----------------------------

async def scrape_site(name: str, url: str, parser_func) -> dict:
    """
    Fetch a site's HTML and parse it with the given parser.
    Returns a dict ready for JSON output.
    """
    timeout = aiohttp.ClientTimeout(total=15)  # be snappy
    connector = aiohttp.TCPConnector(limit=10)  # cap parallel sockets
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        html = await fetch_html(session, url)
        if html is None:
            return {"site": name, "url": url, "ok": False, "items": [], "error": "fetch_failed"}

        try:
            items = await parser_func(html, url)
            return {"site": name, "url": url, "ok": True, "items": items}
        except Exception as parse_err:
            # If custom parser fails, try generic parser so the user still gets something
            try:
                generic_items = await parse_generic_headlines(html, url)
                return {
                    "site": name,
                    "url": url,
                    "ok": True if generic_items else False,
                    "items": generic_items,
                    "error": f"parser_failed: {parse_err.__class__.__name__}",
                }
            except Exception as generic_err:
                return {
                    "site": name,
                    "url": url,
                    "ok": False,
                    "items": [],
                    "error": f"parse_failed: {generic_err.__class__.__name__}",
                }


# -----------------------------
# Menu / Input Helpers
# -----------------------------

def is_valid_url(s: str) -> bool:
    try:
        p = urlparse(s)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False

def show_menu():
    print("\nChoose sites to scrape:")
    for k, v in SITE_REGISTRY.items():
        print(f"  {k}) {v['name']}  ->  {v['url']}")
    print("  a) Add another website URL (generic parser)")
    print("  d) Done (start scraping)")
    print()

async def collect_targets() -> list[tuple[str, str, callable]]:
    """
    Interactive selection:
    - User picks from known sites
    - Can add custom URLs
    Returns a list of (name, url, parser) tuples
    """
    targets: list[tuple[str, str, callable]] = []
    added_any = set()

    while True:
        show_menu()
        choice = input("Your choice (e.g., 1, 2, a, d): ").strip().lower()

        if choice in SITE_REGISTRY:
            site = SITE_REGISTRY[choice]
            name, url, parser = site["name"], site["url"], site["parser"]
            # avoid duplicates
            key = (name, url)
            if key not in added_any:
                targets.append((name, url, parser))
                added_any.add(key)
                print(f"✓ Added {name}")
            else:
                print("Already added.")
        elif choice == "a":
            url = input("Enter website URL (starting with https://): ").strip()
            if not is_valid_url(url):
                print("Invalid URL. Try again.")
                continue
            name = input("Enter a label/name for this website: ").strip() or url
            # generic parser for unknown sites
            targets.append((name, url, parse_generic_headlines))
            print(f"✓ Added custom site: {name} -> {url}")
        elif choice == "d":
            if not targets:
                print("You haven't added any sites yet.")
                continue
            break
        else:
            print("Not a valid choice, try again.")

    return targets


# -----------------------------
# Main
# -----------------------------

async def main():
    print("=== Async Cybersecurity News Scraper ===")
    targets = await collect_targets()

    # Scrape all selected targets concurrently
    tasks = [scrape_site(name, url, parser) for (name, url, parser) in targets]
    results = await asyncio.gather(*tasks)

    # Build final JSON payload
    payload = {
        "ok": True,
        "count": len(results),
        "results": results,
    }

    # Pretty print JSON for humans (machines can read it too)
    print("\n=== JSON Output ===")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # asyncio.run() starts the event loop and runs main()
    asyncio.run(main())
