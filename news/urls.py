from django.urls import path
from .views import FeedCreateView, FeedListView, ArticleListView, ArticleTrendListView

app_name = 'news'
urlpatterns = [
    path('feeds/create', FeedCreateView.as_view(), name='feeds-create'),
    path('feeds/', FeedListView.as_view(), name='feeds-list'),
    path('articles/', ArticleListView.as_view(), name='articles-list'),
    path('trend-articles/', ArticleTrendListView.as_view(), name='articles-trend-list'),
]
