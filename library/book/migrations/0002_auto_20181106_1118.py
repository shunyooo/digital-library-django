# Generated by Django 2.0.8 on 2018-11-06 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='content',
            new_name='category',
        ),
    ]