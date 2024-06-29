# Create your views here.
from django.shortcuts import render
from .models import Article
from django.shortcuts import redirect, get_object_or_404

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'main/article_list.html', {'articles': articles})

def home(request):
    return redirect('article_list')

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'main/article_detail.html', {'article': article})
