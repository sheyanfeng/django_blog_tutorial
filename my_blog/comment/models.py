from django.db import models
from article.models import ArticlePost
from django.contrib.auth.models import User
from django.urls import reverse
class Comment(models.Model):
    #在Comment表上面建立article_id和user_id外键
    # CASCADE外键的级联删除
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        # 取前20字符
        return self.body[:20]


# Create your models here