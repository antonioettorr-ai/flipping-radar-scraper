from playwright.sync_api import sync_playwright


def scrape_idealista():

    listings = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1920, "height": 1080}
        )

        page.goto(
            "https://www.idealista.it/vendita-case/roma/pietralata/",
            wait_until="networkidle",
            timeout=60000
        )

        cards = page.locator("article")

        print("Idealista found:", cards.count())

        for i in range(min(cards.count(), 50)):

            try:

                text = cards.nth(i).inner_text()

                listings.append({
                    "source": "idealista",
                    "title": text[:150],
                    "description": text
                })

            except:
                pass

        browser.close()

    return listings
