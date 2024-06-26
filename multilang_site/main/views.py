# Create your views here.
from django.shortcuts import render
from .models import Article
from django.shortcuts import redirect

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'main/article_list.html', {'articles': articles})

def home(request):
    return redirect('article_list')