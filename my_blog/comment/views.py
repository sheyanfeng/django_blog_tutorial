from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import CommentForm
from article.models import ArticlePost
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    #保证文章存在
    article = get_object_or_404(ArticlePost, id=article_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("输入内容有误，请重新输入")
    else:
        return HttpResponse("发表评论仅接受POST请求")
# Create your views here.
