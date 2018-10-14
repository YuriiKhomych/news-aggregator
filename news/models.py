import re

from django.db import models

from pytrends.request import TrendReq
import feedparser
import dateparser


class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check to see if this is a new feed or not
        new_feed = self.pk is None
        feed_data = feedparser.parse(self.url)
        # Set feed title field if available
        if new_feed:
            if feed_data.feed.title:
                self.title = feed_data.feed.title
            else:
                self.title = "Undefined"
        super(Feed, self).save(*args, **kwargs)
        if new_feed:
            self.get_feed_articles()

    def get_feed_articles(self):
        feed_data = feedparser.parse(self.url)
        for entry in feed_data.entries:
            try:
                article = Article.objects.get(url=entry.link)
            except:
                article = Article()
            article_trend_title = re.sub('[^A-Za-z0-9]+', ' ', entry.title.lower())
            pytrend = TrendReq()
            pytrend.build_payload(kw_list=[article_trend_title])
            interest_over_time_df = pytrend.interest_over_time()
            if not interest_over_time_df.empty:
                article.trend = article_trend_title
            article.title = entry.title
            article.url = entry.link
            published = entry.get('published')
            article.publication_date = dateparser.parse(published) if published else None
            article.feed = self
            article.save()


class Article(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    publication_date = models.DateTimeField(null=True, blank=True)
    trend = models.CharField(max_length=200)

    def __str__(self):
        return self.title
