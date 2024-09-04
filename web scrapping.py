import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the website
BASE_URL = "https://books.toscrape.com/"

# Function to get the HTML content of a page
def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

# Function to parse book details from a page
def parse_books(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    books = []

    for article in soup.find_all('article', class_='product_pod'):
        title = article.h3.a.get('title', 'No title available')
        price = article.find('p', class_='price_color').text
        books.append((title, price))

    return books

# Function to scrape all books from all pages
def scrape_books(base_url):
    books = []
    page_number = 1

    while True:
        print(f"Scraping page {page_number}...")
        url = f"{base_url}catalogue/page-{page_number}.html"
        page_content = get_page_content(url)
        
        if page_content is None:
            break
        
        page_books = parse_books(page_content)
        
        if not page_books:
            break  # No more books, end of pages
        
        books.extend(page_books)
        
        # Check if there's a next page
        soup = BeautifulSoup(page_content, 'html.parser')
        next_button = soup.find('li', class_='next')
        if not next_button:
            break
        
        page_number += 1

    return books

# Main function to save the books data to a CSV file
def save_books_to_csv(books, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Book Name', 'Price'])
        writer.writerows(books)

def main():
    books = scrape_books(BASE_URL)
    save_books_to_csv(books, 'books.csv')
    print("Books data has been saved to 'books.csv'.")

if __name__ == "__main__":
    main()
