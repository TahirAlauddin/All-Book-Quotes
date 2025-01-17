from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from core.models import Quote, Book
import os
import re
from ._add_text_to_image import add_text_to_image
from ._download_images import download_image, random_image_url
from ._decrease_brightness import decrease_brightness

IMAGE_DIRECTORY = 'quotes-images'
DOWNLOADED_IMAGE_DIRECTORY = 'quotes-images-resources'

class Command(BaseCommand):

    help = 'Generate images for Quotes with text on background picture \
using Unsplash API to retrive landscape images.'
    
    def add_arguments(self, parser):
        parser.add_argument('book_slug', nargs='+', type=str)

    def handle(self, *args, **options):
        # If Random images for Quotes Page not exist
        # Create directory and download images
        if not os.path.exists(DOWNLOADED_IMAGE_DIRECTORY):
            os.mkdir(DOWNLOADED_IMAGE_DIRECTORY)
            url = random_image_url()
            for _ in range(200):
                filename = download_image(url, DOWNLOADED_IMAGE_DIRECTORY)
                success = decrease_brightness(filename)
                if success:
                    self.stdout.write(self.style.SUCCESS(f"{filename} downloaded with success!"))

        books_slug = options['book_slug']
        if 'all' in books_slug:
            for slug in Book.objects.values_list('slug', flat=True):
                quotes = Quote.objects.filter(book__slug=slug)
                self.save_quote_images(quotes)
                self.stdout.write(self.style.SUCCESS(f"Quote Images generated successfully for {slug}"))

        else:
            for slug in books_slug:
                quotes = Quote.objects.filter(book__slug=slug)
                self.save_quote_images(quotes)
                self.stdout.write(self.style.SUCCESS(f"Quote Images generated successfully for {slug}"))


    def remove_html_tags(self, text):
        # Remove HTML tags from text
        clean_text = re.sub('<[^<]+?>', '', text)
        return clean_text


    def save_quote_images(self, quotes):
        # Get all images in DOWNLOAD_IMAGE_DIRECTORY, assuming their brightness is already taken care of
        images = os.listdir(DOWNLOADED_IMAGE_DIRECTORY)

        if not os.path.exists(IMAGE_DIRECTORY):
            os.mkdir(IMAGE_DIRECTORY)

        for quote, image in zip(quotes, images):
            image_path = os.path.join(DOWNLOADED_IMAGE_DIRECTORY, image)
            image_path_with_quote = add_text_to_image(self.remove_html_tags(quote.text), image_path)

            if quote.image:
                image_path = quote.image.path
                os.remove(image_path)
                quote.image = None
            
            with open(image_path_with_quote, 'rb') as f:
                quote.image.save(f'{quote.text}.webp', File(f))
                
