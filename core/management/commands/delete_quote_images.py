from django.core.management.base import BaseCommand, CommandError
from core.models import Quote
import os


class Command(BaseCommand):
    
    help = 'Delete old images of quotes and replace with default.'
    

    def handle(self, *args, **options):
        quotes = Quote.objects.all()

        for quote in quotes:
            if quote.image:
                os.remove(quote.image.path)
            quote.image = None
            quote.save()
            self.stdout.write(self.style.SUCCESS(f"{str(quote)} image deleted with success!"))
