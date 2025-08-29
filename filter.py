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

def parse_hackernews(html_content: str) -> list:
    """
    Extracts article titles and links from The Hacker News HTML.

    Args:
        html_content (str): Raw HTML text from thehackernews.com

    Returns:
        list: A list of dicts with 'title' and 'link'
    """
    soup = BeautifulSoup(html_content, "html.parser")
    articles = []

    # On The Hacker News, titles usually have <a> inside h2.story-link or .home-title
    for h2 in soup.find_all("h2", class_="home-title"):
        a = h2.find("a")
        if a and a.get_text(strip=True):
            articles.append({
                "title": a.get_text(strip=True),
                "link": a["href"]
            })

    return articles

def parse_site(site_name: str, html_content: str) -> list:
    """
    Dispatcher: pick the right parser based on site_name.
    """
    if "cybersecuritynews" in site_name :
        print("reached here ")
        return parse_cybersecuritynews(html_content)
    elif "cinemanews" in site_name :
        print("reached here ")
        return parse_cinemanews(html_content)
    elif "thehackernews" in site_name :
        print("reached here ")
        print(html_content)
        return parse_hackernews(html_content)
        file=open("output.txt","w")
        file.write(html_content)
        file.close()
    else:
        raise ValueError(f"No parser available for site: {site_name}")
