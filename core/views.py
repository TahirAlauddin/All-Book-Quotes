from django.db.models.functions import Random
from django.shortcuts import render
from django.conf import settings
from .models import Book, Quote
from .serializers import BookSerializer, QuoteSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response


def index(request):
    return render(request, 'core/home.html')

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
    interesting_books = Book.objects.order_by(Random()).distinct()[:6]
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
    http_method_names = ['get', 'options']

    def list(self, request, *args, **kwargs):
        # Check if the request was made from allbooksquotes.com
        http_referer = request.META.get('HTTP_REFERER', '')
        for allowed_host in settings.ALLOWED_HOSTS:
            if allowed_host in http_referer:
                return super().list(request, *args, **kwargs)
        return Response({'error': 'Unauthorized request'})
    
    def retrieve(self, request, *args, **kwargs):
        # Check if the request was made from allbooksquotes.com
        http_referer = request.META.get('HTTP_REFERER', '')
        for allowed_host in settings.ALLOWED_HOSTS:
            if allowed_host in http_referer:
                return super().retrieve(request, *args, **kwargs)
        return Response({'error': 'Unauthorized request'})
    

class QuoteModelViewSet(ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    http_method_names = ['get', 'options']
    
    def list(self, request, *args, **kwargs):
        # Check if the request was made from allbooksquotes.com
        http_referer = request.META.get('HTTP_REFERER', '')
        for allowed_host in settings.ALLOWED_HOSTS:
            if allowed_host in http_referer:
                return super().list(request, *args, **kwargs)
        return Response({'error': 'Unauthorized request'})
    
    def retrieve(self, request, *args, **kwargs):
        # Check if the request was made from allbooksquotes.com
        http_referer = request.META.get('HTTP_REFERER', '')
        for allowed_host in settings.ALLOWED_HOSTS:
            if allowed_host in http_referer:
                return super().retrieve(request, *args, **kwargs)
        return Response({'error': 'Unauthorized request'})
    