# Generated by Django 2.2 on 2019-04-12 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_auto_20190408_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publisher_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
