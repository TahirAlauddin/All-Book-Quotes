# Generated by Django 4.1.7 on 2023-03-23 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_book_external_link_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='source_or_credit_text',
            field=models.CharField(choices=[('source', 'Source'), ('credit', 'Credit')], max_length=10, null=True, verbose_name='Source or Credit:'),
        ),
    ]
