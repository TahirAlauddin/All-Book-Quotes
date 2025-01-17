# Generated by Django 4.1.7 on 2023-03-21 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_quote_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='book',
            name='external_link',
            field=models.URLField(null=True, verbose_name='External Link'),
        ),
    ]
