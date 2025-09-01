import asyncio
import aiohttp
from bs4 import BeautifulSoup
import hashlib

async def fetch(url):
    """Fetch page HTML from a given URL"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            return await response.text()

def get_structure_signature(html):
    """
    Extract only the HTML structure (tags + class/id names),
    ignoring text content.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # Collect tag name + class/id attributes
    structure = []
    for tag in soup.find_all(True):  # True finds all tags
        signature = (tag.name, tuple(sorted(tag.attrs.keys())))
        structure.append(signature)
    
    # Hash it to compare easily
    return hashlib.md5(str(structure).encode()).hexdigest()

async def main():
    url = input("Enter website URL: ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    # Fetch the site twice
    html1 = await fetch(url)
    html2 = await fetch(url)

    sig1 = get_structure_signature(html1)
    sig2 = get_structure_signature(html2)

    print("First Signature:", sig1)
    print("Second Signature:", sig2)

    if sig1 == sig2:
        print("✅ Structure is the same. Only content may have changed.")
    else:
        print("⚠️ Structure has changed! Scraper might break.")

if __name__ == "__main__":
    asyncio.run(main())
