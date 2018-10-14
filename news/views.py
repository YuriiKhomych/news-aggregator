import re

from django.views.generic import ListView, CreateView
from .forms import FeedForm
from .models import Feed, Article

import dateparser
import feedparser
from pytrends.request import TrendReq


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

    def form_valid(self, form):
        clean_form = form.cleaned_data
        feedparser_data = feedparser.parse(clean_form.get('url'))
        self.object = form.save(commit=False)
        self.object.title = feedparser_data.feed.title
        self.object.save()
        for entry in feedparser_data.entries:
            article_trend_title = re.sub('[^A-Za-z0-9]+', ' ', entry.title.lower())
            pytrend = TrendReq()
            pytrend.build_payload(kw_list=[article_trend_title])
            interest_over_time_df = pytrend.interest_over_time()
            article = Article()
            if not interest_over_time_df.empty:
                article.trend = article_trend_title
            article.title = entry.title
            article.url = entry.link
            published = entry.get('published')
            article.publication_date = dateparser.parse(published) if published else None
            article.feed = self.object
            article.save()
        return super().form_valid(form)
