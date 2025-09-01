def get_user_input() -> tuple[str, str]:
    """
    Ask the user for just a website URL.
    The name will automatically be set to the domain.
    """
    url = input("Enter website URL (e.g., https://thehackernews.com/): ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url   # auto-fix if user forgets

    # Auto-generate site name from URL (domain)
    from urllib.parse import urlparse
    name = urlparse(url).netloc
    return name, url