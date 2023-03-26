from django.db import models
from django.template.defaultfilters import slugify
from .utils import format_number
from django.conf import settings
import os
import random
import string


def get_random_string():
    return ''.join([random.choice(string.ascii_letters + string.digits) 
                    for i in range(6)])

def get_quote_filename(instance, filename):
    """Generate a filename for the uploaded file based on the quote's text"""
    quote_text = slugify(instance.text[:50])  # Generate a slugified version of the quote name
    random_string = get_random_string()
    image_path = os.path.join(settings.QUOTES_MEDIA_PATH, quote_text)
    return f"{image_path}_{random_string}.png"

class SourceCreditChoices(models.Choices):
    SOURCE = 'Source'
    CREDIT = 'Credit'

class Book(models.Model):
    """The Book model also has the following methods:

    __str__: returns a string representation of the book, showing its name.
    save: generates a slugified version of the book's name and saves the model.
    count_quotes: returns the number of quotes related to this book.
    starsHtml: returns a string of HTML code that displays the book's rating as stars.
    votesHtml: returns a string of HTML code that displays the number of votes for the book."""
    
    cover_photo = models.ImageField(upload_to='covers/')
    name = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    rating = models.FloatField(null=True)
    votes = models.BigIntegerField(null=True)
    pages = models.IntegerField(null=True)
    slug = models.SlugField(max_length=255, null=True)
    affiliate_link = models.URLField('Amazon Affiliate Link', null=True, blank=True)
    external_link = models.URLField('External Link', null=True, blank=True)
    external_link_text = models.CharField('External Link Text', max_length=255, null=True, blank=True)
    source_or_credit_text = models.CharField("Source or Credit:", 
                                             choices=SourceCreditChoices.choices, 
                                             max_length=10, null=True, blank=True)
    description = models.TextField("Description", null=True, blank=True)

    def __str__(self):
        return f"<Book name='{self.name}'>"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def count_quotes(self):
        return self.quotes.count()

    @property
    def starsHtml(self):
        stars = '<span class="rating-stars">'
        for i in range(5):
            if i < self.rating:
                stars += '&#9733'
            else:
                stars += '&#9734'
        stars += '</span>'
        return stars
    
    @property
    def votesHtml(self):
        votes = format_number(self.votes).strip()
        return f"({votes} votes)"


class Quote(models.Model):
    """
    The Quote model also has the following methods:

    __str__: returns a string representation of the quote, showing its text.
    save: deletes the old image file when a new image is uploaded and saves the model.
    """
    text = models.TextField()
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='quotes')
    image = models.ImageField(upload_to=get_quote_filename, default='quotes/default-quote.jpg')

    def __str__(self):
        return f"Quote <text={self.text[:50]}...>"
    
    def save(self, *args, **kwargs):
        try:
            this = Quote.objects.get(id=self.id)
            if this.image != self.image:
                os.remove(this.image.path)
                this.image.delete()
        except: pass
        return super().save(*args, **kwargs)
    