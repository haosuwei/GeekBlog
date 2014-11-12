# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import Article


class ExtendedRSSFeed(Rss201rev2Feed):
    mime_type = 'application/xml'
    """
    Create a type of RSS feed that has content:encoded elements.
    """
    def root_attributes(self):
        attrs = super(ExtendedRSSFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])


class LatestArticleFeed(Feed):
    feed_type = ExtendedRSSFeed

    title = settings.WEBSITE_NAME
    link = settings.WEBSITE_URL
    author = settings.WEBSITE_NAME
    description = settings.WEBSITE_NAME + u"关注python、django、vim、linux、web开发和互联网"

    def items(self):
        return Article.objects.filter(hided=False, published=True, sync_status=SYNC_STATUS.SYNCED).order_by('-publish_date')[:10]

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item)}

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_author_name(self, item):
        return item.creator.get_full_name()

    def item_pubdate(self, item):
        return item.create_time

    def item_content_encoded(self, item):
        return item.content
