import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def scrape_thehackernews(session):
    url = "https://thehackernews.com/"
    html_content = await fetch(session, url)
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.select(".story-link")
    return [{"title": a.find("h2").get_text(strip=True), "link": a["href"]} for a in articles[:5]]

async def scrape_cybersecuritynews(session):
    url = "https://cybersecuritynews.com/"
    html_content = await fetch(session, url)
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.select("h3 a")
    return [{"title": a.get_text(strip=True), "link": a["href"]} for a in articles[:5]]

async def scrape(site: str):
    async with aiohttp.ClientSession() as session:
        if site == "thehackernews":
            return await scrape_thehackernews(session)
        elif site == "cybersecuritynews":
            return await scrape_cybersecuritynews(session)
        else:
            return []
