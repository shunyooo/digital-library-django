# Generated by Django 2.0.8 on 2019-04-06 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_book_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
