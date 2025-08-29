# web_fetcher.py
import asyncio
import aiohttp

async def fetch(url: str, save_file: str = "output.txt") -> str:
    """
    Fetch the response text from a given URL asynchronously 
    and save it to a file.

    Args:
        url (str): Website URL to fetch.
        save_file (str): File name to save the response. Default = output.txt.

    Returns:
        str: First 500 characters of the response (for quick preview).
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                text = await response.text()
                print ("request is send")    
                print (f"✅ Fetched {len(text)} characters from {url}")
                return text 
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return ""


async def main(url: str):
    """
    Wrapper to run fetch() with URL correction (auto-add https).
    """
    if not url.startswith("http"):
        url = "https://" + url
    return await fetch(url)


def run(url: str):
    """
    Synchronous entry point to call from another script.
    """
    return asyncio.run(main(url))
