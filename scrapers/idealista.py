from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.idealista.it/vendita-case/roma/pietralata/"

def scrape():

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        html = page.content()

        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/immobile/" in href:

            if href.startswith("/"):
                href = "https://www.idealista.it" + href

            results.append(href)

    return list(set(results))
