from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(User):
    # id = models.AutoField(primary_key=True)
    # hey = models.CharField(max_length=30, default=None, null=True)
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=40)
    # email = models.EmailField()
    # username = models.CharField(max_length=10, unique=True)
    # password = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

class News(models.Model):
    news_id = models.AutoField(primary_key=True, unique=True)
    headline = models.CharField(max_length=64)
    category = models.Choices('pol', 'art', 'tech', 'trivia')
    region = models.Choices('uk', 'eu', 'w')
    author = models.ForeignKey(Author, default=None, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    details = models.CharField(max_length=128)
