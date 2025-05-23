# Generated by Django 5.0.2 on 2024-03-25 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_author_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.author'),
        ),
        migrations.AlterField(
            model_name='author',
            name='hey',
            field=models.CharField(default=None, max_length=30, null=True),
        ),
    ]
