import requests
from bs4 import BeautifulSoup
import re
import json
import os

json_data = []

def write_links(links):
    with open("links.txt", "w", encoding="utf-8") as file:
        for link in links:
            file.write(link + '\n')


def append_json_data(image, book_name, author, pages, rating, votes, quotes):
    # create a dictionary for the row
    row_dict = {
        "image_src": image,
        "book_name": book_name,
        "author": author,
        "pages": pages,
        "rating": rating,
        "votes": votes,
        "quotes": quotes,
    }
    json_data.append(row_dict)


def read_data():
    with open("data.txt", encoding="latin-1") as file:
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


def main():
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

        # Find the votes
        votes = soup.find_all('p')[1].text.split("\n")[3]

        quotes = []

        for quote in soup.select('p.quote[id]'):
            # quote = "\n ".join(str(quote).split('<br/>'))
            quote = "\n" .join(re.split('<br/>|</br>|<br>', str(quote)))

            start_index = quote.index("“")
            end_index = quote.rindex("”")
            quote = quote[start_index:end_index+1]
            quotes.append(quote)

        append_json_data(image_src, book_name, author, pages, rating, votes, quotes)
        write_links(urls[index+1:])
        print(index)


def write_json_data():
    # If file doesn't exist
    if not os.path.exists('books.json'):
        with open('books.json', 'w', encoding='latin-1') as outfile:
            json.dump([], outfile)

    # write the JSON data to a file
    with open("books.json") as infile:
        books = json.load(infile)
    
    with open("books.json", 'w', encoding='latin-1') as outfile:
        books.extend(json_data)
        json.dump(books, outfile, indent=2)


if __name__ == '__main__':
    try:
        main()
    except:
        pass
    write_json_data()
        