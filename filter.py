# news_parser.py
from bs4 import BeautifulSoup

def parse_cybersecuritynews(html_content: str) -> list:
    """
    Parse cybersecuritynews.com HTML and extract article titles + links.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    articles = []
    
    for h2 in soup.find_all("h2"):
        a = h2.find("a")
        if a:
            articles.append({
                "title": a.get_text(strip=True),
                "link": a["href"]
            })
    return articles


def parse_cinemanews(html_content: str) -> list:
    """
    Parse cinemanews HTML and extract article titles + links.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    articles = []
    
    for h3 in soup.find_all("h3"):
        a = h3.find("a")
        if a:
            articles.append({
                "title": a.get_text(strip=True),
                "link": a["href"]
            })
    return articles


def parse_site(site_name: str, html_content: str) -> list:
    """
    Dispatcher: pick the right parser based on site_name.
    """
    if site_name == "cybersecuritynews":
        return parse_cybersecuritynews(html_content)
    elif site_name == "cinemanews":
        return parse_cinemanews(html_content)
    else:
        raise ValueError(f"No parser available for site: {site_name}")
