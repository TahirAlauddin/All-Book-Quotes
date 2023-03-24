from django.urls import path
from .views import *

urlpatterns = [
    path('', list_books, name='home'),
    path('books/<str:slug>-quotes/', get_book_quotes, name='book-quotes'),
    path('about-us/', about_us, name='about-us'),
    path('contact-us/', contact_us, name='contact-us'),
    path('disclaimer/', disclaimer, name='disclaimer'),
    path('copy-right/', copy_right, name='copy-right'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    path('terms-and-conditions/', terms_and_conditions, name='terms-and-conditions'),
    # path('sample', sample)
]