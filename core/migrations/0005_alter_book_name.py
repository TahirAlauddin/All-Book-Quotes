# Generated by Django 4.1.7 on 2023-03-07 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_book_pages_alter_book_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
