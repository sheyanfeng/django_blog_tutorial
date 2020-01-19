from .models import ArticlePost
from django import forms
# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
#内部类，指定字段
    class Meta:
        model = ArticlePost
        fields = ('title', 'body')


# 在ArticlePost模型中，created和updated字段为自动生成，不需要填入；
# author字段暂时固定为id=1的管理员用户，也不用填入；
# 剩下的title和body就是表单需要填入的内容了。




