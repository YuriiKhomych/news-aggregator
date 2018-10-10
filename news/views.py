from django.views.generic import ListView, CreateView
from .forms import FeedForm
from .models import Feed, Article



class ArticleListView(ListView):
    template_name = 'news/articles_list.html'
    queryset = Article.objects.all()


class FeedListView(ListView):
    template_name = 'news/feeds_list.html'
    queryset = Feed.objects.all()


class FeedCreateView(CreateView):
    template_name = 'news/new_feed.html'
    form_class = FeedForm
    queryset = Feed.objects.all()
    success_url = '/news/feeds/'
