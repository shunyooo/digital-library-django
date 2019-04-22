from django.contrib import admin
from .models import Book, Tag, Category, Author, BookImage, WantBook

admin.site.register([Book, Tag, Category, Author, BookImage, WantBook])
