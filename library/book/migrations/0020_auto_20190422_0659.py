# Generated by Django 2.2 on 2019-04-22 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0019_wantbook_caption'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wantbook',
            options={'ordering': ('created_at',)},
        ),
    ]
