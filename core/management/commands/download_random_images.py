from ._download_images import download_image, random_image_url
from django.core.management.base import BaseCommand, CommandError
from ._decrease_brightness import decrease_brightness
import os

DOWNLOADED_IMAGE_DIRECTORY = 'quotes-images-resources'


class Command(BaseCommand):

    help = 'Download images for Quotes using Unsplash API'
    
    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        # Create directory and download images
        if not os.path.exists(DOWNLOADED_IMAGE_DIRECTORY):
            os.mkdir(DOWNLOADED_IMAGE_DIRECTORY)
        url = random_image_url()
        count = options['count']
        for _ in range(count):
            filename = download_image(url, DOWNLOADED_IMAGE_DIRECTORY)
            success = decrease_brightness(filename)
            if success:
                self.stdout.write(self.style.SUCCESS(f"{filename} downloaded with success!"))
