import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.getenv("N8N_WEBHOOK_URL")

URLS = [
    "https://www.idealista.it/vendita-case/roma/pietralata/"
]

def scrape(url):

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    html = requests.get(
        url,
        headers=headers,
        timeout=30
    ).text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    listings = []

    for article in soup.select("article"):

        text = article.get_text(
            " ",
            strip=True
        )

        link = article.find(
            "a",
            href=True
        )

        href = ""

        if link:
            href = link["href"]

            if href.startswith("/"):
                href = (
                    "https://www.idealista.it"
                    + href
                )

        listings.append({
            "source": "idealista",
            "title": text[:150],
            "city": "Roma",
            "zone": "Pietralata",
            "price": 0,
            "sqm": 0,
            "rooms": 0,
            "bathrooms": 0,
            "url": href,
            "description": text
        })

    return listings


def main():

    all_items = []

    for url in URLS:
        all_items.extend(
            scrape(url)
        )

    print(
        "Found:",
        len(all_items)
    )

    if WEBHOOK:
        requests.post(
            WEBHOOK,
            json=all_items,
            timeout=60
        )


if __name__ == "__main__":
    main()
