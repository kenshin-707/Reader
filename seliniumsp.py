from newspaper import Article, build
from newspaper.article import ArticleException


def fetch_articles(url, limit=5):
    """
    Fetch and parse articles from a given news website using newspaper3k.
    :param url: Website URL (e.g., https://techcrunch.com/)
    :param limit: Number of articles to fetch
    :return: List of article details
    """
    try:
        # Build a newspaper source object
        paper = build(url, memoize_articles=False)

        news_list = []
        for i, article in enumerate(paper.articles[:limit], start=1):
            try:
                article.download()
                article.parse()
                article.nlp()  # Extract summary & keywords

                news_list.append({
                    "headline": article.title or "No Title",
                    "summary": article.summary or "No Summary",
                    "link": article.url,
                    "date": article.publish_date.strftime("%Y-%m-%d %H:%M:%S") if article.publish_date else "No Date"
                })
            except ArticleException as e:
                print(f"[Warning] Skipped article {i}: {e}")
                continue

        return news_list

    except Exception as e:
        print(f"[Error] Failed to fetch articles: {e}")
        return []


def display_news(news_list):
    """
    Print articles in a clean, formatted way.
    """
    if not news_list:
        print("[Info] No articles found.")
        return

    for idx, news in enumerate(news_list, start=1):
        print(f"\n📰 Article {idx}")
        print(f"Headline: {news['headline']}")
        print(f"Summary : {news['summary']}")
        print(f"Date    : {news['date']}")
        print(f"Link    : {news['link']}")
        print("-" * 60)


def main():
    url = "https://techcrunch.com/"  # You can replace with any news site
    print(f"[Info] Fetching latest articles from {url}")
    articles = fetch_articles(url, limit=5)  # Limit to 5 articles
    display_news(articles)


if __name__ == "__main__":
    main()
