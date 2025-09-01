import asyncio
import json
import aiohttp

from req import fetch_html
from filterz import parse_generic_headlines
from voice_input import get_voice_input


async def scrape_site(name: str, url: str) -> dict:
    """
    Fetch + parse one site (always uses generic parser here).
    """
    timeout = aiohttp.ClientTimeout(total=15)
    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        html = await fetch_html(session, url)
        if html is None:
            return {"site": name, "url": url, "ok": False, "items": [], "error": "fetch_failed"}

        try:
            if name in ("The Hacker News", "thehackernews.com"):
                from filterz import parse_thehackernews
                items = await parse_thehackernews(html, url)
                return {"site": name, "url": url, "ok": bool(items), "items": items}
            elif name in ("CyberSecurityNews", "cybersecuritynews.com"):
                from filterz import parse_cybersecuritynews
                items = await parse_cybersecuritynews(html, url)
                return {"site": name, "url": url, "ok": bool(items), "items": items}
            elif name in ("trading platforms", "fxstreet.com"):
                from filterz import parse_fxstreetnews
                items = await parse_fxstreetnews(html, url)
                return {"site": name, "url": url, "ok": bool(items), "items": items}
            else:
                items = await parse_generic_headlines(html, url)
                return {"site": name, "url": url, "ok": bool(items), "items": items}
        except Exception as e:
            return {"site": name, "url": url, "ok": False, "items": [], "error": str(e)}


async def main():
    name, url = get_voice_input()
    result = await scrape_site(name, url)
    print("\n=== JSON Output ===")
    for i, item in enumerate(result.get("items", []), start=1):
      print(f"{i}. {item['title']}")
      print(f"   {item['link']}\n")


if __name__ == "__main__":
    asyncio.run(main())
