# Generated by Django 5.0.2 on 2024-03-25 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_news_author_alter_author_hey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='hey',
        ),
    ]
