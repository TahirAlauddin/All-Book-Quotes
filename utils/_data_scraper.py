import requests
from bs4 import BeautifulSoup


def write_links(data):
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write("|")
        for i in data:
            file.write("~" + i)


def write_data(image, book_name, author, pages, rating, votes):
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(image + "|" + book_name + "|" + author +
                   "|" + pages + "|" + rating + "|" + votes)


def read_data():
    with open("data.txt", encoding="utf-8") as file:
        data = file.readlines()

        return data


def read_links():
    with open("links.txt") as file:
        data = file.readlines()

        cleaned_data = []
        for i in data:
            cleaned_data.append(i.strip())

        return cleaned_data


prefix_url = "https://bookquoters.com/"

urls = read_links()
for index, url in enumerate(urls):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the image source
    image_src = soup.find('div', {'class': 'header_bg'}).find('img')['src']
    image_src = prefix_url + image_src[1:]

    # Find the book name
    book_name = soup.find('h1').text.strip().replace(
        "Quotes from", "").strip()

    # Find the number of pages
    author = soup.find('span', {'class': 'color_gray'}
                        ).text.strip().split("\n")[0].strip()
    author = " ".join(author.split()[:-1])

    pages = soup.find('p').text.split()[-2:][0]

    # Find the rating
    rating = soup.find('span', {'class': 'ui stars rating'})['data-rating']

    votes = soup.find_all('p')[1].text.split("\n")[3]

    quote_text = soup.find(
        'p', {'class': 'quote'}).text.strip().split("\n")[0]

    quotes = []

    for quote in soup.find_all('p', {'class': 'quote'}):
        quotes.append(quote.text.strip().split("\n")[0])

    write_data(image_src, book_name, author, pages, rating, votes)
    write_links(quotes)
    with open("data.txt", "a") as file:
        file.write("\n")

    print(index)
