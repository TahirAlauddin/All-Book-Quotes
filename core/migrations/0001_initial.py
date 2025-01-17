# Generated by Django 4.1.7 on 2023-03-07 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_photo', models.ImageField(upload_to='covers/')),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
                ('votes', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.book')),
            ],
        ),
    ]
