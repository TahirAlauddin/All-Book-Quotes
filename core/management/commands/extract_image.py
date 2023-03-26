from django.core.management.base import BaseCommand
from PIL import Image
import json
import io
import os
import requests
import re
import os

IMAGE_DIRECTORY = 'quotes-images'
DOWNLOADED_IMAGE_DIRECTORY = 'quotes-images-resources'

class Command(BaseCommand):

    help = 'Download images from the links provided in json file.'
    
    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
                
        # Create a directory to save the images in
        if not os.path.exists('Images'):
            os.mkdir('Images')
        if not os.path.exists('images_saved.txt'):
            open('images_saved.txt', 'w').close

        # Open the JSON file and load its contents into a Python object
        with open(options.get('json_file', 'books.json')) as file:
            links_data = json.load(file)

        images_saved = []
        with open('images_saved.txt') as f:
            for line in f.readlines():
                images_saved.append(line.strip())

        try:
            for link in links_data:
                if link['book_name'] in images_saved:
                    continue
                response = requests.get(link["image_src"])

                # Create a PIL image object from the binary data
                pil_image = Image.open(io.BytesIO(response.content))

                # Save the image as a WEBP file
                cleaned_str = "Images/" + remove_special_chars(link["book_name"]) + " Image.webp"
                pil_image.save(cleaned_str, format="webp")
                book_name = link['book_name']
                images_saved.append(book_name)
                self.stdout.write(self.style.SUCCESS(f"Cover image for {book_name} saved with success!"))

        except Exception:
            with open('images_saved.txt', 'w') as f:
                for image in images_saved:
                    f.write(image + '\n')


def remove_special_chars(input_string):
    # Define the regular expression pattern to match special characters
    pattern = r'[^\w\s]'

    # Use the sub() function to replace all special characters with an empty string
    output_string = re.sub(pattern, '', input_string)

    return output_string


