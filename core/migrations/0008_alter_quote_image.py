# Generated by Django 4.1.7 on 2023-03-11 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_quote_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='image',
            field=models.ImageField(default='quotes/default-quote.webp', upload_to='quotes/'),
        ),
    ]
