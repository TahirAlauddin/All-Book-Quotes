from django.shortcuts import render
from .models import Book, Quote
from .serializers import BookSerializer, QuoteSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
import random
# import django_filters.rest_framework import 

def get_book(request, slug):
    book = Book.objects.get(slug=slug)
    return render(request, 'core/book.html', context={'book': book})

def list_books(request):
    books = Book.objects.all()[:20]
    return render(request, 'core/home.html', context={'books': books})


def contact_us(request):
    return render(request, 'core/contact-us.html')


def about_us(request):
    return render(request, 'core/about-us.html')

def disclaimer(request):
    return render(request, 'core/disclaimer.html')

def copy_right(request):
    return render(request, 'core/copyright.html')

def privacy_policy(request):
    return render(request, 'core/privacy-policy.html')


def terms_and_conditions(request):
    return render(request, 'core/terms-and-conditions.html')


def get_book_quotes(request, slug):
    quotes = Quote.objects.filter(book__slug=slug)
    interesting_books = Book.objects.all()
    interesting_books = [random.choice(interesting_books) for i in range(6)]
    search_filter = request.GET.get('search')
    if search_filter:
        quotes = quotes.filter(text__icontains=search_filter)
    return render(request, 'core/quotes.html', 
                  {'quotes': quotes,
                   'interesting_books': interesting_books,
                   'book': Book.objects.get(slug=slug)})


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', 'author']


class QuoteModelViewSet(ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    