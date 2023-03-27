from django.db.models.functions import Random
from django.shortcuts import render
from django.conf import settings
from .models import Book, Quote
from .serializers import BookSerializer, QuoteSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.views.decorators.cache import cache_page

@cache_page(5 * 60)
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

@cache_page(5 * 60)
def get_book_quotes(request, slug):
    return render(request, 'core/quotes.html', {'book': Book.objects.get(slug=slug)})


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', 'author']
    http_method_names = ['get', 'options']

    def list(self, request, *args, **kwargs):
        # Check if the request was made from allbooksquotes.com
        random = request.query_params.get('random')
        http_referer = request.META.get('HTTP_REFERER', '')
        for allowed_host in settings.ALLOWED_HOSTS:
            if allowed_host in http_referer:
                if random:
                    self.queryset = Book.objects.order_by(Random()).distinct()[:6]
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
    serializer_class = QuoteSerializer
    http_method_names = ['get', 'options']
    filter_backends = [SearchFilter]
    search_fields = ['text']
    http_method_names = ['get', 'options']


    def get_queryset(self):
        book_filter = self.kwargs['book_slug']
        queryset = Quote.objects.filter(book__slug=book_filter)
        return queryset
    
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
    