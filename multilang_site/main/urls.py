from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('change_language/', views.change_language, name='change_language'),
    path('chatbot/', views.chatbot, name='chatbot'),
       path('search/', views.search_with_rag, name='search_with_rag'),
]
