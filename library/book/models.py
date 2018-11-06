from django.db import models


# Create your models here.
class Tag(models.Model):
    """タグ."""
    content = models.CharField(max_length=255, unique=True, db_index=True)
    book_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.content


class Category(models.Model):
    """カテゴリ."""
    content = models.CharField('カテゴリ名', max_length=255)
    book_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.content


class Author(models.Model):
    """著者."""
    name = models.CharField(max_length=200)
    book_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """本."""
    title = models.CharField(max_length=200, unique=True)
    page_count = models.PositiveIntegerField()
    author = models.ManyToManyField(Author, related_name='books')
    tag = models.ManyToManyField(Tag, related_name='books')
    content = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
