from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
class ArticlePost(models.Model):
    """
    文章作者。参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。
    使用 ForeignKey定义一个关系。这将告诉 Django，每个（或多个） ArticlePost 对象
    都关联到一个 User 对象。Django本身具有一个简单完整的账号系统（User），足以满
    足一般网站的账号申请、建立、权限、群组等基本功能。
    用户=作者，两者关联起来，括号里面表示是“一”

    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)
    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()
    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    #浏览量：存储正整数的字段
    total_views = models.PositiveIntegerField(default=0)


    # 内部类 class Meta 用于给 model 定义元数据(外加功能)
    class Meta:
        """ordering 指定模型返回的数据的排列顺序
            保证了最新的文章总是在网页的最上方
        """
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
# Create your models here.
