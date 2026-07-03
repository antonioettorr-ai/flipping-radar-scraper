from playwright.sync_api import sync_playwright

URL = "https://www.idealista.it/vendita-case/roma/pietralata/"

def scrape_idealista():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137 Safari/537.36"
        )

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        html = page.content()

        print(html[:3000])

        browser.close()

    return []
