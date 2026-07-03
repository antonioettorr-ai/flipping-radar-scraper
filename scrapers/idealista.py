from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.idealista.it/vendita-case/roma/pietralata/"


def scrape_idealista():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1920, "height": 1080}
        )

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/immobile/" in href:
            if href.startswith("/"):
                href = "https://www.idealista.it" + href

            links.add(href.split("?")[0])

    for href in links:
        results.append({
            "source": "idealista",
            "city": "Roma",
            "zone": "Pietralata",
            "title": "Annuncio Idealista",
            "price": 0,
            "sqm": 0,
            "rooms": 0,
            "bathrooms": 0,
            "url": href,
            "description": ""
        })

    print("Idealista links:", len(results))

    return results
