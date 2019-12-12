from django.shortcuts import render, redirect
from django.http import HttpResponse
# 导入数据模型类
from .models import ArticlePost, User
# 导入markdown
import markdown
# 导入表单类
from .forms import ArticlePostForm
# 导入分页类
from django.core.paginator import Paginator
# 检测用户登录的装饰器
from django.contrib.auth.decorators import login_required
# 导入Q对象
from django.db.models import Q
# 导入评论模型
from comment.models import Comment
# strip_tags去掉html文本的全部HTML标签
from django.utils.html import strip_tags

# Create your views here.


def article_list(request):  # 文章列表
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            article_all = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_all = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_all = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_all = ArticlePost.objects.all()
    md = markdown.Markdown(extensions=[
        # 包含缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 包含代码代码高亮扩展
        'markdown.extensions.codehilite',
    ])
    paginator = Paginator(article_all, 10)  # 对所有文章对象进行分页处理
    page = request.GET.get('page')  # 获取翻页按钮上的url的页码参数
    articles = paginator.get_page(page)
    for article in articles:
        article.body = strip_tags(md.convert(article.body))

    context = {'articles': articles, 'order': order, 'search': search}
    return render(request, 'article/list.html', context)


def article_detail(request, id):  # 文章内容
    article = ArticlePost.objects.get(id=id)
    md = markdown.Markdown(extensions=[
        # 包含缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 包含代码高亮扩展
        'markdown.extensions.codehilite',
        # 目录
        'markdown.extensions.toc',
    ])
    article.body = md.convert(article.body)
    # 将markdown语法渲染成html样式
    # article.body = markdown.markdown(article.body, extensions=[
    #     # 包含缩写、表格等常用扩展
    #     'markdown.extensions.extra',
    #     # 包含代码高亮扩展
    #     'markdown.extensions.codehilite',
    #     ])
    # 计算阅读量
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 取出文章对应的评论
    comments = Comment.objects.filter(article_id=id)
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):  # 撰写文章
    if request.method == 'POST':
        # 获取前端提交过来的数据，绑定表单
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 如果表单提交过来的数据是有效的
        if article_post_form.is_valid():
            # 将表单数据保存生成一条新的数据对象，但是并不提交
            new_article = article_post_form.save(commit=False)
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse('提交的数据有误，请重新提交')
    else:
        article_post_form = ArticlePostForm()
        authors = User.objects.all()
        context = {'article_post_form': article_post_form, 'authors': authors}
        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):  # 删除文章
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:  # 验证是否是作者本人操作
            return HttpResponse('您无权做此操作')
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('不是post的请求')


@login_required(login_url='/userprofile/login/')
def article_update(request, id):  # 更新文章
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('提交的数据有误')
    else:
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:  # 验证是否是作者本人操作
            return HttpResponse('您无权做此操作')
        article_dict = ArticlePost.objects.get(id=id).__dict__
        article_post_form = ArticlePostForm(article_dict)
        authors = User.objects.all()
        context = {'article_post_form': article_post_form, 'authors': authors, 'article': article}
        return render(request, 'article/update.html', context)

