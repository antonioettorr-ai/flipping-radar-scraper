import os
import re
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.getenv("N8N_WEBHOOK_URL")

URLS = [
    "https://www.idealista.it/vendita-case/roma/pietralata/"
]

def to_number(text):
    if not text:
        return 0
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else 0

def scrape(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8"
    }

    response = requests.get(url, headers=headers, timeout=30)
    html = response.text

    print("Status:", response.status_code)
    print("HTML length:", len(html))

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("article.item")
    if not cards:
        cards = soup.select("[data-element-id]")
    if not cards:
        cards = soup.select(".item")

    listings = []

    for card in cards:
        text = card.get_text(" ", strip=True)

        link = card.find("a", href=True)
        href = link["href"] if link else ""

        if href.startswith("/"):
            href = "https://www.idealista.it" + href

        title_el = card.select_one(".item-link")
        price_el = card.select_one(".item-price")
        detail_els = card.select(".item-detail")

        title = title_el.get_text(" ", strip=True) if title_el else text[:120]
        price = to_number(price_el.get_text(" ", strip=True)) if price_el else 0

        sqm = 0
        rooms = 0
        bathrooms = 0

        for d in detail_els:
            dt = d.get_text(" ", strip=True).lower()
            if "m²" in dt or "mq" in dt:
                sqm = to_number(dt)
            elif "local" in dt:
                rooms = to_number(dt)
            elif "bagno" in dt:
                bathrooms = to_number(dt)

        if href or title:
            listings.append({
                "source": "idealista",
                "title": title,
                "city": "Roma",
                "zone": "Pietralata",
                "price": price,
                "sqm": sqm,
                "rooms": rooms,
                "bathrooms": bathrooms,
                "balcony": "balcone" in text.lower(),
                "elevator": "ascensore" in text.lower(),
                "metro_distance": 9999,
                "url": href,
                "description": text
            })

    return listings

def main():
    all_items = []

    for url in URLS:
        all_items.extend(scrape(url))

    print("Found:", len(all_items))

    if WEBHOOK and all_items:
        r = requests.post(WEBHOOK, json=all_items, timeout=60)
        print("Webhook status:", r.status_code)
        print("Webhook response:", r.text[:300])

if __name__ == "__main__":
    main()
