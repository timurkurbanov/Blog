from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

min_length = MinLengthValidator(limit_value=2)

class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(validators=[min_length])
    draft = models.BooleanField()
    published_date = models.DateField(help_text='yyyy-mm-dd')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topics")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    def __str__(self):
        return self.title

    def sort_comment_set(self):
        return self.comments.order_by('created_at')

class Comment(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.message
