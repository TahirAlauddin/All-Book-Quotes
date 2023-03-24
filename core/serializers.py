from rest_framework.serializers import ModelSerializer
from .models import Book, Quote

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'cover_photo', 'name', 'author', 'rating',
                  'votes', 'pages', 'slug', 'affiliate_link',
                  'description',]
        lookup_field = 'slug'

class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quote
        fields = ['text']

