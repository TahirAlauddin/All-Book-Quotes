from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.files import File
from core.models import Book, Quote  
import json
import os
import re


def remove_special_chars(input_string):
    # Define the regular expression pattern to match special characters
    pattern = r'[^\w\s]'

    # Use the sub() function to replace all special characters with an empty string
    output_string = re.sub(pattern, '', input_string)

    return output_string


def parse_number(number_string):
    number_string = number_string.split(' ')[0]
    if number_string[-1] == 'M':
        multiplier = 1000000
    elif number_string[-1] == 'K':
        multiplier = 1000
    else:
        multiplier = 1

    number = number_string.split()[0][:-1]
    if number:
        return int(float(number) * multiplier)
    return 0


class Command(BaseCommand):
    
    help = 'Generate images for Quotes with text on background picture \
using Unsplash API to retrive landscape images.'
    
    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options.get('path', 'books_data.json')

        self.populate_db_from_json(path)


    def populate_db_from_json(self, json_path):
        # open the JSON file and load data
        with open(json_path, 'r') as f:
            books_data = json.load(f)

        # Get a list of all book names in the database
        book_names = list(Book.objects.values_list('name', flat=True))

        # iterate over each book in the data and create a new Django model object
        for book_data in books_data:
            if book_data['book_name'] in book_names:
                continue

            book = Book()    # set the image field
            image_path = fr"Images/{remove_special_chars(book_data['book_name'])} Image.webp"
            try:
                with open(image_path, 'rb') as f:
                    image_name = os.path.basename(image_path)
                    book.cover_photo.save(image_name, File(f))
            except FileNotFoundError:
                self.stderr.write(self.style.ERROR(f"{str(book)} image file not found!"))      
                continue

            if not book_data['book_name']:
                continue
            book.name = book_data['book_name']
            book.author = book_data['author']
            book.pages = book_data['pages']
            book.rating = book_data['rating']
            book.votes = parse_number(book_data['votes'].strip('()'))
            book.save()  # save the new model object to the database
            book_names.append(book.name)

            # add quotes to the book
            for quote_text in book_data['quotes']:
                if not quote_text:
                    continue
                quote = Quote()
                quote.text = quote_text
                quote.book = book
                quote.save()

            self.stdout.write(self.style.SUCCESS(f"{str(book)} saved with success!"))
