from django.db import models
from article.models import ArticlePost
from django.contrib.auth.models import User


# Create your models here.

class Comment(models.Model):
    # ForeignKey是一对多，一个文章肯定是关联多个评论的
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    # ForeignKey是一对多，一个用户肯定是关联多个评论的
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.body[:20]
