# Generated by Django 4.1.7 on 2023-03-07 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_book_rating_alter_book_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
