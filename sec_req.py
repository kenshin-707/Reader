import asyncio
from req import fetch_html
from submain import scrape_site
# Your JSON data
data = {'site': 'www.fxstreet.com', 'url': 'https://www.fxstreet.com/news', 'ok': True, 'items': [{'title': 'AUD/USD struggles to extend upside above 0.6550 ahead of US PCE inflation data', 'link': 'https://www.fxstreet.com/currencies/audusd'}, {'title': 'EUR/USD: Buyers gain confidence ahead of the Nonfarm Payrolls report', 'link': 'https://www.fxstreet.com/analysis/eur-usd-weekly-forecast-buyers-gain-confidence-ahead-of-the-nonfarm-payrolls-report-202508291509'}, {'title': 'UPCOMING CALENDAR EVENTS', 'link': 'https://www.fxstreet.com/economic-calendar'}, {'title': 'Gold: Sellers remain on sidelines on dovish Fed expectations, geopolitics', 'link': 'https://www.fxstreet.com/markets/commodities/metals/gold'}, {'title': 'Week ahead: All eyes on NFP report as Fed rate cut bets intensify', 'link': 'https://www.fxstreet.com/analysis/week-ahead-all-eyes-on-nfp-report-as-fed-rate-cut-bets-intensify-video-202508291323'}, {'title': 'After earnings sell-off, Nvidia stock regains $180', 'link': 'https://www.fxstreet.com/news/after-earnings-sell-off-nvidia-stock-regains-180-202508281820'}, {'title': 'PRESS RELEASES', 'link': 'https://www.fxstreet.com/press-releases'}, {'title': 'Make better decisions: T4Trade’s approach to responsible trading', 'link': 'https://www.fxstreet.com/press-releases/make-better-decisions-t4trades-approach-to-responsible-trading-202508290649'}, {'title': 'Prop Firms Evolve in 2025: Adapting to New Technology and Trader Needs', 'link': 'https://www.fxstreet.com/press-releases/prop-firms-evolve-in-2025-adapting-to-new-technology-and-trader-needs-202508281338'}, {'title': '15 Years of IronFX: Recognised for Innovation and Trust', 'link': 'https://www.fxstreet.com/press-releases/15-years-of-ironfx-recognised-for-innovation-and-trust-202508281328'}]}

# You already have this function in your project
# async def scrape_site(name: str, url: str) -> dict: ...

async def main():
    # Show all available articles
    print("Available articles:\n")
    for i, item in enumerate(data["items"], start=1):
        print(f"{i}. {item['title']}")

    # User picks one
    choice = int(input("\nEnter the number of the article you want: ")) - 1
    if 0 <= choice < len(data["items"]):
        selected = data["items"][choice]
        print(f"\nFetching: {selected['title']}\n")

        # Call your existing scraper
        result = await scrape_site(data["site"], selected["link"])

        print("=== Scraped Content ===\n")
        print(result)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    asyncio.run(main())
