from .views import subscriptions
from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.NewsList.as_view(), name='news_list'),
    path('news/search/', views.search, name='news_search'),
    path('news/<int:pk>/', views.NewsDetail.as_view(), name='news_detail'),
    path('news/create/', views.NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', views.ArticlesCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticlesUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticlesDelete.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]