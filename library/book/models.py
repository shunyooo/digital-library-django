from django.urls import reverse
from django.db import models

from book.constants import BOOK_STATUS_CREATED
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def default_category():
    """デフォルトのカテゴリを返す(まだなければ作る)."""
    category, _ = Category.objects.get_or_create(content='未設定')
    return category.pk


def default_tag():
    """デフォルトのタグ達を返す(まだなければ作る)."""
    tag, _ = Tag.objects.get_or_create(content='未設定')
    return tag


def default_author():
    """デフォルトの著者を返す(まだなければ作る)."""
    author, _ = Author.objects.get_or_create(name='未設定')
    return author


# Create your models here.
class Tag(models.Model):
    """タグ."""
    content = models.CharField(max_length=255, unique=True, db_index=True)
    book_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('content',)

    def __str__(self):
        return self.content


class Category(models.Model):
    """カテゴリ."""
    content = models.CharField('カテゴリ名', unique=True, max_length=255)
    book_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.content


class Author(models.Model):
    """著者."""
    name = models.CharField(max_length=200, unique=True)
    book_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """本."""
    title = models.CharField(max_length=200, unique=True)
    pdf_file = models.FileField(max_length=500, null=True)
    zip_file = models.FileField(max_length=500, null=True)
    thumbnail_origin_image = models.ImageField(max_length=500, null=True)
    thumbnail_image = ImageSpecField(source='thumbnail_origin_image',
                                     format='JPEG',
                                     options={'quality': 60})

    page_count = models.PositiveIntegerField()
    author = models.ManyToManyField(Author, related_name='books', default=default_author, )
    tag = models.ManyToManyField(Tag, related_name='books', default=default_tag, )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books', default=default_category, )
    status = models.IntegerField(default=BOOK_STATUS_CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # info系
    description = models.TextField(null=True)
    isbn = models.CharField(max_length=200, unique=True, null=True)
    sub_title = models.CharField(max_length=500, null=True)
    price = models.PositiveIntegerField(default=0)
    sales_at = models.DateTimeField(auto_now=True, null=True)
    publisher_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('created_at',)


class BookImage(models.Model):
    """本のイメージ"""
    image = models.ImageField(max_length=500)
    page = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images', )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['page']
