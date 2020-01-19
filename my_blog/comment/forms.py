# 表单：提交数据

from django import forms
from .models import Comment
# 写评论的表单类
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']