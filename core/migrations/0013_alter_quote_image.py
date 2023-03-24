# Generated by Django 4.1.7 on 2023-03-24 10:40

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_book_source_or_credit_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='image',
            field=models.ImageField(default='quotes/default-quote.jpg', upload_to=core.models.get_quote_filename),
        ),
    ]
