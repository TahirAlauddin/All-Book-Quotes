from django.core.files.storage import default_storage
from django.contrib import admin
from django.db.models.signals import pre_save
from .models import *

class QuoteAdmin(admin.ModelAdmin):
    search_fields = ('text', 'book__name')

class QuoteInline(admin.TabularInline):
    model = Quote

class BookAdmin(admin.ModelAdmin):
    inlines = [QuoteInline]
    fields = ('cover_photo', 'affiliate_link', 'name', 'author', 'rating',
              'votes', 'pages', 'slug', 'description', 'external_link',
               'external_link_text', 'source_or_credit_text')
    list_display = ('name', 'author', 'pages', 'affiliate_link')
    list_filter = ('rating',)
    search_fields = ('name',)

admin.site.register(Book, BookAdmin)
admin.site.register(Quote, QuoteAdmin)
