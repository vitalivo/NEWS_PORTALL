from .views import subscriptions
from django.urls import include, path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'post', views.PostViewset)
router.register(r'category', views.CategoryViewset)
router.register(r'comment', views.CommentViewset)
router.register(r'author', views.AuthorViewSet)


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
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

