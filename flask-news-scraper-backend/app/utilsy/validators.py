import re

ALLOWED_SITES = ["hackernews", "thehackernews", "bleepingcomputer"]

def validate_site(site):
    return site in ALLOWED_SITES

def sanitize_keyword(keyword):
    keyword = re.sub(r"[^a-zA-Z0-9\s\-]", "", keyword)  # remove special chars
    return keyword.strip()
