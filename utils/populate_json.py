import json
import os
from django.db.utils import IntegrityError
from django.core.files import File
from core.models import Book, Quote  # replace `myapp` with your Django app name
import re


def remove_special_chars(input_string):
    # Define the regular expression pattern to match special characters
    pattern = r'[^\w\s]'

    # Use the sub() function to replace all special characters with an empty string
    output_string = re.sub(pattern, '', input_string)

    return output_string


def parse_number(number_string):
    if number_string[-1] == 'M':
        multiplier = 1000000
    elif number_string[-1] == 'K':
        multiplier = 1000
    else:
        multiplier = 1

    number = number_string.split()[0][1:-1]
    if number:
        return int(float(number) * multiplier)
    return 0


# open the JSON file
with open('books_data.json', 'r') as f:
    books_data = json.load(f)

book_names = []

books = Book.objects.all()
for book in books:
    book_names.append(book.name)


# iterate over each book in the data and create a new Django model object
for book_data in books_data:

    if book_data['book_name'] in book_names:
        continue

    book = Book()    # set the image field
    image_path = fr"Images/{remove_special_chars(book_data['book_name'])} Image.jpg"
    print(image_path)

    try:
        with open(image_path, 'rb') as f:
            image_name = os.path.basename(image_path)
            book.cover_photo.save(image_name, File(f))
    except FileNotFoundError:
        continue

    book.name = book_data['book_name']
    book_names.append(book.name)
    book.author = book_data['author']
    book.pages = book_data['pages'] if type(book_data, int) else 100
    book.rating = book_data['rating'] if type(book_data, int) else 3
    book.votes = parse_number(book_data['votes'].strip('()'))
    book.save()  # save the new model object to the database

    # add quotes to the book
    for quote_text in book_data['quotes']:
        if not quote_text:
            continue
        quote = Quote()
        quote.text = quote_text
        quote.book = book
        quote.save()

