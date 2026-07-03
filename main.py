from scrapers.idealista import scrape

items = scrape()

print("Found:", len(items))

for x in items:
    print(x)
