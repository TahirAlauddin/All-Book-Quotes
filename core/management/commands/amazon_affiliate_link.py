from core.models import Book
from django.core.management.base import BaseCommand, CommandError
from _search_amazon import search_items


class Command(BaseCommand):
    
    help = 'Add Amazon Affiliate Link to the Book'
    
    def add_arguments(self, parser):
        parser.add_argument('book_slug', nargs='+', type=str)

    def handle(self, *args, **options):
        books_slug = options['book_slug']
        if '*' in books_slug:
            for book in Book.objects.all():
                self.save_affiliate_link(book)

        else:
            for slug in books_slug:
                book = Book.objects.filter(book__slug=slug).first()
                if book:
                    self.save_affiliate_link(book)

    def save_affiliate_link(self, book):
        link = search_items(book.name)
        if link:
            book.affiliate_link = link
            book.save()
        self.stdout.write(self.style.SUCCESS(f"Amazon Affiliate Link for {book.name} saved!"))
