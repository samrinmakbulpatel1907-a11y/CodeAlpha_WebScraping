
import requests
from bs4 import BeautifulSoup
import csv

# Public demo website
url = "https://books.toscrape.com/"

try:
    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    data = []

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").get_text(strip=True)
        availability = book.find(
            "p", class_="instock availability"
        ).get_text(strip=True)

        data.append([title, price, availability])

    # Save results to CSV
    with open("scraped_books.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Book Title", "Price", "Availability"])
        writer.writerows(data)

    print("WEB SCRAPING COMPLETED!")
    print("Total books scraped:", len(data))
    print("Data saved to scraped_books.csv")

    print("\nFirst 5 books:")
    for row in data[:5]:
        print("Title:", row[0])
        print("Price:", row[1])
        print("Availability:", row[2])
        print("-" * 30)

except requests.RequestException as error:
    print("Website request failed:", error)
