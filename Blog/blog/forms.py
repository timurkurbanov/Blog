from blog.models import Article, Comment
from datetime import date, datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, PasswordInput
from pytz import timezone

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'draft', 'published_date', 'topic']

    def clean_published_date(self):
        # localizing both dates
        publishedDate = self.cleaned_data['published_date']
        presentDate = date.fromtimestamp(datetime.now(timezone('America/Toronto')).timestamp())
        print(presentDate)
        print(publishedDate)
        isDraft = self.cleaned_data['draft']
        if isDraft:
            if publishedDate < presentDate:
                raise ValidationError('Specified date must be in the future!')
            else:
                return publishedDate
        else:
            if publishedDate > presentDate:
                raise ValidationError('Specified date must be in the past!')
            else:
                return publishedDate
