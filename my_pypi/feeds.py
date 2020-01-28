from django.contrib.syndication.views import Feed
from article.models import ArticlePost
from django.urls import reverse
# import feedparser


class LatestEntriesFeed(Feed):
    title = "我皮网的博客"
    link = "/feed/"
    description = "最新博客文章"

    def items(self):
        return ArticlePost.objects.order_by('-created')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('article:article_detail', args=[item.id, ])  # 重点是'article:article_detail'怎么理解


# d = feedparser.parse('https://rssfeed.today/weibo/rss/1623873051')
#
# print(d['feed']['title'])
