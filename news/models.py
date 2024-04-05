from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(User):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

class News(models.Model):
    CategoryChoices = (
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivial)')
    )
    news_id = models.AutoField(primary_key=True, unique=True)
    headline = models.CharField(max_length=64)
    category = models.CharField(choices=CategoryChoices, max_length=10, default='trivia')
    region = models.CharField(choices=(('uk', 'United Kingdom'), ('eu', 'Europe'), ('w', 'World')), max_length=10, default='w')
    author = models.ForeignKey(Author, default=None, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now=True)
    details = models.CharField(max_length=128)

    def __str__(self):
        categories = dict(self.CategoryChoices)
        return f"{self.headline} - {categories[self.category]} - {self.author}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News'"
