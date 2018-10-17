from __future__ import absolute_import, unicode_literals

from .models import Feed

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task()
def update_all_feed_articles_task():
    """ Updates articles for all RSS/Atom feeds """
    feeds = Feed.objects.all()
    for feed in feeds:
        logger.info(f"Retrieving Articles for {feed.title}")
        feed.get_feed_articles()
    logger.info(f"Finished Retrieving Articles for {feed.title}")
