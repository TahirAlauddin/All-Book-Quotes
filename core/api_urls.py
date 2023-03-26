from django.urls import path, include
from rest_framework_nested import routers
from .views import *

books_router = routers.DefaultRouter()
books_router.register('books', BookModelViewSet, basename='books')

quotes_router = routers.NestedDefaultRouter(books_router, 'books', lookup='book')
quotes_router.register('quotes', QuoteModelViewSet, basename='book-quotes')

urlpatterns = [
    path('', include(books_router.urls)),
    # path('', include(quotes_router.urls)),
]