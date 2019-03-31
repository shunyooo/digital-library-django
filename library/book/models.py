from django.urls import reverse
from django.db import models

from book.constants import BOOK_STATUS_CREATED

from taggit.managers import TaggableManager


def default_category():
    """デフォルトのカテゴリを返す(まだなければ作る)."""
    category, _ = Category.objects.get_or_create(content='未設定')
    return category.pk


def default_author():
    """デフォルトの著者を返す(まだなければ作る)."""
    author, _ = Author.objects.get_or_create(name='未設定')
    return author


class Category(models.Model):
    """カテゴリ."""
    content = models.CharField('カテゴリ名', unique=True, max_length=255)
    book_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.content


class Author(models.Model):
    """著者."""
    name = models.CharField(max_length=200, unique=True)
    book_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """本."""
    title = models.CharField(max_length=200, unique=True)
    pdf_file = models.FileField(max_length=500, null=True)
    zip_file = models.FileField(max_length=500, null=True)
    page_count = models.PositiveIntegerField()
    author = models.ManyToManyField(Author, related_name='books', default=default_author, )
    tags = TaggableManager()

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books', default=default_category, )
    status = models.IntegerField(default=BOOK_STATUS_CREATED)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book:detail', kwargs={'pk': self.pk})


class BookImage(models.Model):
    """本のイメージ"""
    image = models.ImageField(max_length=500)
    page = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images', )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['page']
