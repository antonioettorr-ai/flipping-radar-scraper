
import os
import requests

from scrapers.idealista import scrape_idealista

WEBHOOK = os.getenv("N8N_WEBHOOK_URL")


def main():

    listings = []

    try:
        listings.extend(scrape_idealista())
    except Exception as e:
        print("Idealista error:", e)

    print("TOTAL:", len(listings))

    if WEBHOOK and listings:

        r = requests.post(
            WEBHOOK,
            json=listings,
            timeout=60
        )

        print("Webhook:", r.status_code)


if __name__ == "__main__":
    main()
