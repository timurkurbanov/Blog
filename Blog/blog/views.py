from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from blog.models import Article, Comment, Topic
from blog.forms import CommentForm, ArticleForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()
    context = {'title': 'Log in', 'form': form}
    html_response = render(request, 'login.html', context)
    return HttpResponse(html_response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'title': 'Sign up', 'form': form})
    return HttpResponse(html_response)

def posts_page(request):
    context = {'title': "The Blog", 'articles': Article.objects.filter(draft=False).order_by('-published_date')}
    html_string = render(request, 'posts.html', context)
    return HttpResponse(html_string)

def post_show(request, id):
    post = Article.objects.get(pk=id)
    context = {'title': post.title, 'post': post, 'comment_form':CommentForm()}
    html_string = render(request, 'post.html', context)
    return HttpResponse(html_string)

@login_required
def new_post(request):
    context = {'title':'Create a new post', 'article_form': ArticleForm()}
    html_string = render(request, 'new_post.html', context)
    return HttpResponse(html_string)

@login_required
def create_post(request):
    form = ArticleForm(request.POST)
    if form.is_valid():
        new_article = form.instance
        new_article.user = request.user
        new_article.save()
        return HttpResponseRedirect("/posts/")
    else:
        html_string = render(request, 'new_post.html', {'title': 'Create a new post', 'article_form': ArticleForm(request.POST)})
        return HttpResponse(html_string)

@login_required
def edit_post(request, id):
    post = get_object_or_404(Article, pk=id, user=request.user.pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=post)
        if form.is_valid():
            updated_post = form.save()
            return HttpResponseRedirect(reverse('post_details', args=[post.id]))
    else:
        form = ArticleForm(instance=post)
    context = {'title': 'Edit Post', 'form': form, 'post': post}
    html_response = render(request, "edit_post.html", context)
    return HttpResponse(html_response)

def user_posts(request):
    user_articles = request.user.articles
    context = {'title': "The Blog", 'articles': user_articles.filter(draft=False).order_by('-published_date')}
    html_string = render(request, 'posts.html', context)
    return HttpResponse(html_string)

def create_comment(request):
    article = Article.objects.get(pk=request.POST['post_id'])
    form = CommentForm(request.POST)
    path = '/posts/' + str(article.pk)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.article = article
        new_comment.save()
        return HttpResponseRedirect(path)
    else:
        print(form.errors)

def root(request):
    return HttpResponseRedirect('/posts/')
