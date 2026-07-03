import os
import requests

from scrapers.idealista import scrape_idealista

WEBHOOK = os.getenv("N8N_WEBHOOK_URL")


def main():
    listings = []

    try:
        idealista_items = scrape_idealista()
        listings.extend(idealista_items)
    except Exception as e:
        print("Idealista error:", e)

    print("Found:", len(listings))

    if WEBHOOK and listings:
        response = requests.post(
            WEBHOOK,
            json=listings,
            timeout=60
        )
        print("Webhook status:", response.status_code)


if __name__ == "__main__":
    main()
