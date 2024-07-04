from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "Latest Posts"
    link = "/blog/rss/"
    description = "Updates on the latest posts on the blog."

    def items(self):
        return Post.objects.order_by('-created_on')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('blog_detail', args=[item.pk])
