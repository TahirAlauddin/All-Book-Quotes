from rest_framework.serializers import ModelSerializer
from .models import Book, Quote


class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quote
        fields = ['text', 'image']


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'cover_photo', 'name', 'author', 'rating',
                  'votes', 'pages', 'slug', 'affiliate_link',
                  'description', 'source_or_credit_text', 'external_link',
                   'external_link_text']
        lookup_field = 'slug'


