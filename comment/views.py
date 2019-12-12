from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CommentForm
from .models import Comment, ArticlePost
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/userprofile/login/')
def comment_post(request, id):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        article = ArticlePost.objects.get(id=id)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('提交的数据验证失败')
    else:
        return HttpResponse('仅支持POST请求')


