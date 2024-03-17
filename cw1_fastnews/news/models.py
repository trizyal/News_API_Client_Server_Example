from django.db import models

# Create your models here.
class Author(models.Model):
    author_id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=30)

class News(models.Model):
    news_id = models.AutoField(primary_key=True, unique=True)
    headline = models.CharField(max_length=64)
    category = models.Choices('pol', 'art', 'tech', 'trivia')
    region = models.Choices('uk', 'eu', 'w')
    author = models.ManyToManyField(Author)
    date = models.DateField()
    details = models.CharField(max_length=128)
