import asyncio
import aiohttp

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

async def fetch_html(session: aiohttp.ClientSession, url: str, *, max_retries: int = 2) -> str | None:
    """Download HTML with retries + timeout handling."""
    for attempt in range(max_retries + 1):
        try:
            async with session.get(url, headers=DEFAULT_HEADERS) as resp:
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
                print(f"⚠️ Warning: failed to fetch {url}: {e}")
                return None
