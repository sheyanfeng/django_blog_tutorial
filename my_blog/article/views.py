from comment.models import Comment
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost
import markdown
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        article_list = ArticlePost.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''
        article_list = ArticlePost.objects.all()
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    else:
        pass
    #用户搜索逻辑
    # if search:
    #     if order == 'total_views':
    #         # 用 Q对象 进行联合搜索
    #         article_list = ArticlePost.objects.filter(
    #             Q(title__icontains=search) |
    #             Q(body__icontains=search)
    #         ).order_by('-total_views')
    #     else:
    #         article_list = ArticlePost.objects.filter(
    #             Q(title__icontains=search) |
    #             Q(body__icontains=search)
    #         )
    # else:
    # # 将 search 参数重置为空
    #     search = ''
    #     if order == 'total_views':
    #         article_list = ArticlePost.objects.all().order_by('-total_views')
    #     else:
    #         article_list = ArticlePost.objects.all()

    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 9)
    # 获取 url 中的页码
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = { 'articles': articles, 'order': order, 'search':search }
    return render(request, 'article/list.html', context)

# 文章详情

def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    #取出文章评论
    comments = Comment.objects.filter(article=id)
    #浏览量加1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # # 需要传递给模板的对象
    '''

    第一个参数是需要渲染的文章正文article.body
    第二个参数载入了常用的语法扩展，markdown.extensions.extra中包括了缩写、表格等扩展，
    markdown.extensions.codehilite则是后面要使用的代码高亮扩展。
    '''
    # article.body = markdown.markdown(article.body,
    #     extensions=[
    #     # 包含 缩写、表格等常用扩展
    #     'markdown.extensions.extra',
    #     # 语法高亮扩展
    #     'markdown.extensions.codehilite',
    #     #目录扩展
    #     'markdown.extensions.toc',
    #     ])
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    '''
    先将Markdown类赋值给一个临时变量md，然后用convert()
    方法将正文渲染为html页面。通过md.toc将目录传递给模板。
    '''

    article.body = md.convert(article.body)
    # 传到前端

    context = { 'article': article, 'toc': md.toc, 'comments': comments }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("文章为空！")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article_post_form': article_post_form }
        return render(request, 'article/create.html', context)


"""
当视图函数接收到一个客户端的request请求时，首先根据request.method判断用户是要提交数据（POST）、还是要获取数据（GET）：

如果用户是提交数据，将POST给服务器的表单数据赋于article_post_form实例。

然后使用Django内置的方法.is_valid()判断提交的数据是否满足模型的要求。

如果满足要求，保存表单中的数据（但是commit=False暂时不提交到数据库，因为author还未指定），并指定author为id=1的管理员用户。
然后提交到数据库，并通过redirect返回文章列表。redirect可通过url地址的名字，反向解析到对应的url。

如果不满足要求，则返回一个字符串"表单内容有误，请重新填写。"，告诉用户出现了什么问题。

如果用户是获取数据，则返回一个空的表单类对象，提供给用户填写。

"""
@login_required(login_url='/userprofile/login/')
def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    else:
        article.delete()
        return redirect("article:article_list")

def article_safe_delete(request,id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许POST请求")
#过滤未登录用户
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
# 旧的整个对象的数据
    article = ArticlePost.objects.get(id=id)
#过滤非作者用户
    if request.user != article.author:
        return  HttpResponse("抱歉，你无权修改这篇文章。")
# 新添加的数据
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article': article, 'article_post_form': article_post_form }
        return render(request, 'article/update.html', context)


